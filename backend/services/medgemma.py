from datetime import datetime, date
import os
import asyncio
from beanie import PydanticObjectId
from beanie.operators import Or
from typing import List
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from contracts import (GeneratedQuestion, InvestigationDecision, ClinicalSuggestion,
                       PatientHistoryItem, TriageData, UnityContextSnapshot,
                       ServiceSheetDetail, TriageInvestigationQA)

class MedGemmaProvider:
    """
    Provides orchestration and inference capabilities using the MedGemma AI model.

    This class acts as an Anti-Corruption Layer (ACL) between the strict data schemas
    of the backend (Pydantic/Beanie) and the generative output of the local LLM inference
    engine (Ollama). It manages prompt construction, execution chains, and Data Transfer
    Object (DTO) mapping for all three phases of the AI-assisted clinical triage workflow.

    Attributes:
        _ollama_base_url (str): The inference server URL, fetched from the environment 
            variable 'OLLAMA_BASE_URL' to support dynamic Docker networking.
        llm (OllamaLLM): The LangChain connector instance configured for the MedGemma model.
        parser_phase_one (PydanticOutputParser): Parser to enforce JSON structure for Phase 1.
        parser_phase_two (PydanticOutputParser): Parser to enforce JSON structure for Phase 2.
    """
    
    _ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    _ollama_model = os.getenv("OLLAMA_MODEL")
    
    llm = OllamaLLM(
        model=_ollama_model,
        base_url=_ollama_base_url,
        temperature=0.1
    )

    parser_phase_one = PydanticOutputParser(pydantic_object=InvestigationDecision)
    parser_phase_two = PydanticOutputParser(pydantic_object=ClinicalSuggestion)

    @staticmethod
    def _format_history_text(history: List[PatientHistoryItem]) -> str:
        """
        Formats the patient's longitudinal history into a dense text block.

        Args:
            history (List[PatientHistoryItem]): List of past service sheets.

        Returns:
            str: Formatted history string.
        """
        
        if not history: 
            return "Longitudinal History: No previous records in this unit (New Patient)"
            
        formatted_blocks = []
        
        for idx, item in enumerate(history):
            triage_data = item.triage_data
            doctor_data = item.doctor_data
            vitals = triage_data.vitals if triage_data else None

            block = [f"### PREVIOUS SERVICE {idx + 1} (Data: {item.created_at.strftime('%d/%m/%Y %H:%M')})"]

            if vitals:
                vitals_line = f"VITALS: PA {vitals.systolic_bp}/{vitals.diastolic_bp} mmHg | FC {vitals.heart_rate} bpm | Temp {vitals.temperature}°C | SpO2 {vitals.oxygen_saturation}%"
                if vitals.extras:
                    extras_str = ", ".join([f"{k}: {v}" for k, v in vitals.extras.items()])
                    vitals_line += f" | Additional Information: {extras_str}"
                block.append(vitals_line)

            if triage_data:
                block.append(f"Complaint to the Nurse: {triage_data.nurse_initial_observations}")

                if triage_data.investigation_qa:
                    for qa in triage_data.investigation_qa:
                        if qa.patient_answer:
                            block.append(f"  - Question: {qa.question_text} | Answer: {qa.patient_answer}")

                block.append(f"Final Classification: {triage_data.risk_classification.upper() if triage_data.risk_classification else 'N/A'}")
                if triage_data.final_nurse_notes:
                    block.append(f"Nursing Final Notes: {triage_data.final_nurse_notes}")

            if doctor_data:
                block.append(f"MEDICAL OUTCOME: CID {doctor_data.diagnosis_cid or 'Not Informed'}")
                block.append(f"Doctor's Notes: {doctor_data.doctor_notes}")
                if doctor_data.prescription:
                    block.append(f"Medical Prescription: {doctor_data.prescription}")

            formatted_blocks.append("\n".join(block))

        return "\n\n".join(formatted_blocks)

    @staticmethod
    def _format_current_context(triage_data: TriageData) -> str:
        """
        Formats the current patient entry data.

        Args:
            triage_data (TriageData): Current triage data.

        Returns:
            str: Formatted current status string.
        """
        vitals = triage_data.vitals
        block = ["### PATIENT'S CURRENT STATUS (ENTER NOW)"]

        vitals_line = f"VITALS: PA {vitals.systolic_bp}/{vitals.diastolic_bp} mmHg | FC {vitals.heart_rate} bpm | Temp {vitals.temperature}°C | SpO2 {vitals.oxygen_saturation}%"
        if vitals.extras:
            extras_str = ", ".join([f"{k}: {v}" for k, v in vitals.extras.items()])
            vitals_line += f" | Additional Information: {extras_str}"
        block.append(vitals_line)

        block.append(f"Initial Complaint to The Nurse: {triage_data.nurse_initial_observations}")
        return "\n".join(block)

    @staticmethod
    def _format_unit_context(unity_history: UnityContextSnapshot) -> str:
        """
        Formats the hospital unit's environmental context.

        Args:
            unity_history (UnityContextSnapshot): Unit context data.

        Returns:
            str: Formatted unit status string.
        """
        return f"### UNIT STATUS\nCurrent Crowding: {unity_history.crowding_level.upper()}"

    @classmethod
    def assemble_clinical_context(cls, triage_data: TriageData, patient_history: List[PatientHistoryItem], unity_history: UnityContextSnapshot) -> str:
        """
        Orchestrates the assembly of the final text following the hierarchy:
        1. Current Status -> 2. History -> 3. Unit Status.

        Args:
            triage_data (TriageData): Current triage data.
            patient_history (List[PatientHistoryItem]): Patient's clinical history.
            unity_history (UnityContextSnapshot): Unit context data.

        Returns:
            str: The full clinical context assembled.
        """
        current = cls._format_current_context(triage_data)
        history = cls._format_history_text(patient_history)
        unit = cls._format_unit_context(unity_history)

        return f"{current}\n\n{history}\n\n{unit}"

    @classmethod
    async def orchestrate_investigation(cls, triage_data: TriageData, patient_history: List[PatientHistoryItem], unity_history: UnityContextSnapshot) -> List[TriageInvestigationQA]:
        """
        PHASE 1: Analyzes clinical context to decide if investigation questions are needed.

        Args:
            triage_data (TriageData): Current triage data.
            patient_history (List[PatientHistoryItem]): Patient's clinical history.
            unity_history (UnityContextSnapshot): Unit context data.

        Returns:
            InvestigationDecision: Structured output containing the decision and generated questions.
        """
        context = cls.assemble_clinical_context(triage_data, patient_history, unity_history)

        prompt = PromptTemplate(
            template="""
You are MedGemma, a high-fidelity clinical triage agent specializing in standard 5-level clinical triage protocols (e.g., ESI, Manchester-style color tracking) and longitudinal patient analysis.
Your objective is to assist the nursing staff by identifying latent clinical risks that are NOT obvious from the current observation but become apparent when cross-referencing with the patient's history.

ANALYSIS MANDATE:
1. LONGITUDINAL CROSS-REFERENCE: Compare current vitals and complaints with previous CIDs, medications, and clinical outcomes found in the history.
2. LATENT RISK DETECTION: Identify "Red Flags" associated with the patient's chronic conditions or past procedures (e.g., prior stents, diabetes, renal failure) that were not explicitly addressed in the current 'Queixa Inicial'.
3. INSIGHT GENERATION: Formulate questions that provide diagnostic insights for the doctor and safety for the nurse. Avoid generic questions like "How are you feeling?".
4. UNIT CONTEXT AWARENESS: Consider the current crowding level ({crowding_level}). If CRITICAL, prioritize questions that rule out immediate life-threatening conditions.
5. DYNAMIC QUANTITY: Choose between 0 and 5 questions based on diagnostic uncertainty. If the risk is clearly immediate (e.g., suspected active AMI), set 'needs_investigation' to false and justify in 'reasoning'.
6. EXPLICIT CITATION: Whenever a question is motivated by past data, you MUST extract and cite the exact historical data point (e.g., 'CID I20.8 on dd/mm/aaaa', 'headache on dd/mm/aaaa', 'medication x in dd/mm/aaaa' ) in the 'historical_reference' field.
7. STRICT ANTI-REDUNDANCY (CRITICAL): You MUST treat the 'Dados Extras' as EXHAUSTIVE and COMPLETE. If an anatomical region or symptom category (e.g., pain radiation) is mentioned, DO NOT attempt to expand on it by asking about other body parts. Assume the nurse has already mapped the entire region. Asking expanding questions on already mapped symptoms is a critical system failure.

OUTPUT REQUIREMENTS:
- All 'question_text' and 'ai_reasoning' MUST be written in professional Brazilian Portuguese (PT-BR).
- The 'ai_reasoning' should explain concisely and assertively the clinical correlation between the historical data and the current presentation.

CLINICAL CONTEXT:
{full_context}

{format_instructions}

Final Constraint: Output ONLY the raw JSON object. Do not include any conversational filler.
""",
            input_variables=["full_context", "crowding_level"],
            partial_variables={"format_instructions": cls.parser_phase_one.get_format_instructions()}
        )

        chain = prompt | cls.llm | cls.parser_phase_one

        try:
            result = await chain.ainvoke({
                "full_context": context,
                "crowding_level": unity_history.crowding_level
            })
            
            if not result.needs_investigation:
                return []
            
            final_qa_list = []
            for q in result.questions:
                final_qa_list.append(
                    TriageInvestigationQA(
                        question_id=PydanticObjectId(),
                        question_text=q.question_text,
                        ai_reasoning=q.ai_reasoning,
                        patient_answer=None
                    )
                )
            return final_qa_list

        except Exception as e:
            return []

    @classmethod
    async def generate_clinical_suggestion(cls, triage_data: TriageData, patient_history: List[PatientHistoryItem], unity_history: UnityContextSnapshot) -> str:
        """
        PHASE 2: Consumes the Phase 1 answers and generates the final triage risk suggestion.

        Args:
            triage_data (TriageData): Current triage data including investigation QA.
            patient_history (List[PatientHistoryItem]): Patient's clinical history.
            unity_history (UnityContextSnapshot): Unit context data.

        Returns:
            str: Markdown formatted string containing the risk color and clinical summary.
        """
        contexto = cls.assemble_clinical_context(triage_data, patient_history, unity_history)

        respostas = ""
        if triage_data.investigation_qa:
            respostas = "\n".join([f"Q: {qa.question_text} | A: {qa.patient_answer}" for qa in triage_data.investigation_qa if qa.patient_answer])
        if not respostas:
            respostas = "Nenhuma pergunta adicional foi respondida."

        prompt = PromptTemplate(
            template="""
You are MedGemma, a senior clinical auditor. Your task is to perform the FINAL TRIAGE CLASSIFICATION based on standard 5-level clinical severity guidelines.

ANALYSIS MANDATE:
1. SYNTHESIS: Evaluate the patient's current vitals, longitudinal history, and the newly answered investigation questions.
2. RISK STRATIFICATION: Assign the correct risk color based strictly on clinical severity (Vermelho = immediate life threat, Laranja = very urgent, Amarelo = urgent, Verde = standard, Azul = non-urgent).
3. CLINICAL SUMMARY: Write a concise bullet-point summary for the triage nurse, explaining WHY this color was chosen.
4. DOCTOR ALERTS: Highlight specific warning signs (e.g., "Risk of acute MI", "Patient is hypertensive and non-compliant") for the doctor.

OUTPUT REQUIREMENTS:
- All text MUST be in professional Brazilian Portuguese (PT-BR).

CLINICAL CONTEXT:
{full_context}

NEW INVESTIGATION ANSWERS (Phase 1):
{answers_phase_one}

{format_instructions}

Final Constraint: Output ONLY the raw JSON object. Do not include any conversational filler.
""",
            input_variables=["full_context", "answers_phase_one"],
            partial_variables={"format_instructions": cls.parser_phase_two.get_format_instructions()}
        )

        chain = prompt | cls.llm | cls.parser_phase_two

        try:
            result = await chain.ainvoke({
                "full_context": contexto,
                "answers_phase_one": respostas
            })
            markdown_output = f"### Risk Suggestion: {result.risk_color.upper()}\n\n"
            markdown_output += f"**Technical Summary:**\n{result.technical_summary}\n\n"
            markdown_output += "**Observation Points for the Nurse:**\n"
            for point in result.observation_points:
                markdown_output += f"- {point}\n"

            return markdown_output

        except Exception as e:
            return f"Error generating medical suggestion: {str(e)}"

    @classmethod
    async def generate_doctor_summary(cls, sheet_details: ServiceSheetDetail) -> str:
        """
        PHASE 3: Generates a concise handover summary for the attending doctor.
        Designed to be run asynchronously via a background task queue.

        Args:
            sheet (ServiceSheet): The finalized service sheet containing triage data.

        Returns:
            str: A short, 3-sentence plain text clinical summary.
        """
        triage_data = sheet_details.triage_data
        patient_data = sheet_details.patient

        if not triage_data:
            return "Insufficient triage data for summary."

        context_parts = []

        hoje = date.today()
        nascimento = patient_data.birth_date
        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))

        acompanhante_str = "With companion" if patient_data.companion else "Without companion"
        context_parts.append(f"PATIENT DEMOGRAPHICS: {idade} years, Sex: {patient_data.sex.value}, {acompanhante_str}.")

        vitals = triage_data.vitals
        vitals_line = f"VITALS: PA {vitals.systolic_bp}/{vitals.diastolic_bp} mmHg | FC {vitals.heart_rate} bpm | Temp {vitals.temperature}°C | SpO2 {vitals.oxygen_saturation}%"
        if vitals.extras:
            extras_str = ", ".join([f"{k}: {v}" for k, v in vitals.extras.items()])
            vitals_line += f" | Additional Information: {extras_str}"
        context_parts.append(vitals_line)

        context_parts.append(f"Initial Complaint to The Nurse: {triage_data.nurse_initial_observations}")

        if triage_data.investigation_qa:
            qa_texts = []
            for qa in triage_data.investigation_qa:
                if qa.patient_answer:
                    qa_texts.append(f"Q: {qa.question_text} | A: {qa.patient_answer}")

            if qa_texts:
                context_parts.append("AI Investigation Responses:\n" + "\n".join(qa_texts))

        if hasattr(triage_data, 'ai_generated_suggestion') and triage_data.ai_generated_suggestion:
            context_parts.append(f"AI Generated Clinical Suggestions: {triage_data.ai_generated_suggestion}")
        elif hasattr(triage_data, 'ai_generated_sugestion') and triage_data.ai_generated_sugestion:
            context_parts.append(f"AI Generated Clinical Suggestions: {triage_data.ai_generated_sugestion}")

        context_parts.append(f"Final Risk Classification: {triage_data.risk_classification.upper() if triage_data.risk_classification else 'N/A'}")

        if triage_data.final_nurse_notes:
            context_parts.append(f"Nursing Final Notes: {triage_data.final_nurse_notes}")

        sheet_context = "\n\n".join(context_parts)

        prompt_phase3 = PromptTemplate(
            template="""
You are MedGemma. Generate a highly concise, 3-paraghaph clinical handoff summary for the attending doctor.

DATA:
{sheet_context}

RULES:
- Language: Professional Brazilian Portuguese (PT-BR).
- Format: Plain text only. No markdown, no bullet points, no conversational intro.
- Focus: Synthesize using the SBAR (Situation, Context, Assessment, Recommendation) methodology for patient's demographics (age/sex), chief complaint, critical vitals (and extras), the most relevant answers from the investigation, and the final risk assessment.
""",
            input_variables=["sheet_context"]
        )

        chain = prompt_phase3 | cls.llm

        try:
            summary = await chain.ainvoke({"sheet_context": sheet_context})
            return summary.strip()
        except Exception as e:
            return f"Erro ao gerar resumo médico: {str(e)}"