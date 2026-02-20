from datetime import datetime
import asyncio
from beanie import PydanticObjectId
from beanie.operators import Or
from fastapi import HTTPException
from typing import Optional, List
from models import User, Patient, ServiceSheet
from contracts import (PatientUpdate, TriageDataPhaseOne, TriageDataPhaseTwo,
                        TriageDataPhaseThree, TriageInvestigationQA, UnityContextSnapshot,
                        TriageData, PatientHistoryItem)

class MedGemmaProvider:
    """
    Encapsula o Agente MedGemma e atua como um provedor de sugestões.
    
    TODO 1: orchestrate_investigation(triage_data: TriageData, patient_history: List[PatientHistoryItem], unit_context: UnityContextSnapshot) -> List[TriageInvestigationQA]
        - MÉTODO PÚBLICO (Usado na Fase 1).
        - Atua como o decisor.
        - Passo 1: Chama _decide_investigation_need().
        - Se a decisão for não perguntar: Retorna lista vazia [].
        - Se a decisão for perguntar: Chama _generate_questions() passando a quantidade decidida.
        - Retorna a lista de objetos TriageInvestigationQA.

    TODO 2: _decide_investigation_need(context_data) -> Dict
        - MÉTODO PRIVADO (Interno do Agente).
        - Analisa a entropia/incerteza do caso.
        - Prompt focada em raciocínio clínico
        - Retorna: {"needs_investigation": bool, "num_questions": int, "reasoning": str}

    TODO 3: _generate_questions(context_data, num_questions: int) -> List[TriageInvestigationQA]
        - MÉTODO PRIVADO (Interno do Agente).
        - Só é chamado se o TODO 2 for True.
        - Gera as perguntas específicas baseadas no raciocínio anterior.
        - Garante que a saída esteja no formato JSON estrito para virar objeto Pydantic.

    TODO 4: generate_medical_suggestion(triage_data: TriageData) -> str
        - MÉTODO PÚBLICO (Usado na Fase 2).
        - Compila todo o contexto + as respostas que o paciente deu.
        - Gera um texto técnico em bullet points (seguindo a lógica Médico para Enfermeiro) sugerindo a hipótese diagnóstica e pontos de atenção. São sugestões e podem ser modificadas.

    TODO 5: generate_doctor_summary(sheet: ServiceSheet) -> str
        - MÉTODO PÚBLICO (Usado na Fase 3 e na fila de maneira assíncrona).
        - Gera o resumo técnico para o médico.
        - Resume o caso focando no auxílo à tomada de decisão rápida.
    """

    @staticmethod
    async def orchestrate_investigation(triage_data: TriageData, patient_history: List[PatientHistoryItem], unity_history: UnityContextSnapshot) -> List[TriageInvestigationQA]:
        
        return await MedGemmaProvider._generate_questions(context_data=triage_data, num_questions=2)

    @staticmethod
    async def _generate_questions(context_data, num_questions: int) -> List[TriageInvestigationQA]:
        
        questions = []
        for i in range(num_questions):
            questions.append(
                TriageInvestigationQA(
                    question_id=PydanticObjectId(),
                    question_text=f"Pergunta simulada {i+1} pela IA. O paciente sente dor?",
                    ai_reasoning=f"Raciocínio simulado {i+1}: Investigar possível quadro agudo."
                )
            )
        return questions
    
    @staticmethod
    async def generate_medical_suggestion(triage_data: TriageData, patient_history: List[PatientHistoryItem], unity_history: UnityContextSnapshot) -> str:
        
        return (
            "**Sugestão Diagnóstica (Mock IA):**\n"
            "- Possível infecção viral respiratória baseada na temperatura (febre) e saturação.\n"
            "- Observar frequência cardíaca elevada.\n"
            "\n*Nota: Esta é uma simulação gerada para testes de interface.*"
        )
    
    @staticmethod
    async def generate_doctor_summary(sheet: ServiceSheet) -> str:

        summary = "Resumo automatizado do caso. Paciente apresentou febre e dores."
        
        if sheet.doctor_data:
            sheet.doctor_data.ai_pre_consultation_summary = summary
        else:
            # Requer import do DoctorData se for fazer isso
            pass 
            
        return summary