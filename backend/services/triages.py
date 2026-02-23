from datetime import datetime
import asyncio
from beanie import PydanticObjectId
from beanie.operators import In, Set, Or, And
from fastapi import HTTPException
from typing import Optional, List
from models import User, Patient, ServiceSheet, TriageStatus
from contracts import (
    TriageDataPhaseOne, TriageDataPhaseTwo,
    TriageDataPhaseThree, TriageInvestigationQA, UnityContextSnapshot,
    TriageQueueItem, ServiceSheetDetail, TriageData, PatientCreate)
from services.patients import PatientService
from services.medgemma import MedGemmaProvider
from exceptions import (
    ServiceSheetNotFoundError, NurseNotFoundError, 
    InvalidTriageStateError, IncompleteTriageDataError, PatientNotFoundError
)

class TriageService:
    """
    Orchestrates the triage workflow, managing data persistence and AI integration.

    This service encapsulates the state machine for a patient's journey through 
    the triage sector, coordinating inputs from the nursing staff, contextual 
    data retrieval (history and crowding), and interactions with the MedGemmaProvider.

    Dependencies:
        - PatientService: For historical data extraction.
        - MedGemmaProvider: For LLM reasoning and generation.
    """
    
    @staticmethod
    async def get_triage_queue(nurse_id: PydanticObjectId) -> List[TriageQueueItem]:
        """
        Retrieves the queue of patients waiting for triage and active sessions for the nurse.

        Fetches active service sheets sorted by arrival time First-In-First-Out (FIFO).
        The query uses logical operators to fetch:
        1. All sheets globally waiting for triage.
        2. Sheets currently in a triage phase strictly assigned to the requesting nurse.
        
        Uses batch processing to retrieve patient names via an O(1) memory map, 
        preventing N+1 query bottlenecks.

        Args:
            nurse_id: The unique database ID of the nurse requesting the queue.

        Returns:
            A list of TriageQueueItem objects representing the waiting/active patients.
        """
        
        sheets = await ServiceSheet.find(
            Or(
                ServiceSheet.status == TriageStatus.aguardando_triagem,
                And(
                    ServiceSheet.nurse_ref == nurse_id,
                    In(ServiceSheet.status, [
                        TriageStatus.em_triagem_fase_1,
                        TriageStatus.em_triagem_fase_2,
                        TriageStatus.em_triagem_fase_3
                    ])
                )
            )
        ).sort(ServiceSheet.created_at).to_list()
        
        if not sheets:
            return []
        
        patient_ids = [sheet.patient_ref for sheet in sheets]
        
        patients = await Patient.find(In(Patient.id, patient_ids)).to_list()
        
        patient_map = {patient.id: patient.name for patient in patients}
        
        queue = []
        
        for sheet in sheets:
            queue.append(TriageQueueItem(
                sheet_id=sheet.id,
                patient_id=sheet.patient_ref,
                patient_name=patient_map.get(sheet.patient_ref, "Unknown"),
                arrival_time=sheet.created_at,
                status=sheet.status
            ))
        
        return queue

    @staticmethod
    async def _calculate_unit_context() -> UnityContextSnapshot:
        """
        Calculates the current crowding level of the triage unit. Based on an arbitrary 
        occupancy condition for example purposes.

        Executes an optimized count query for active patients (waiting or currently 
        in triage) to provide environmental context for the MedGemma AI decision engine.

        Returns:
            A UnityContextSnapshot containing the crowding level string and timestamp.
        """
        
        number_of_sheets = await ServiceSheet.find(
            In(ServiceSheet.status, [
                TriageStatus.aguardando_triagem,
                TriageStatus.em_triagem_fase_1,
                TriageStatus.em_triagem_fase_2,
                TriageStatus.em_triagem_fase_3
            ])
        ).count()
        
        if number_of_sheets < 10:
            crowding_level = "low"
        elif number_of_sheets < 20:
            crowding_level = "medium"
        elif number_of_sheets < 30:
            crowding_level = "high"
        else:
            crowding_level = "critical"
        
        return UnityContextSnapshot(
            crowding_level=crowding_level,
            captured_at=datetime.now()
            )
    
    @staticmethod
    async def start_triage(sheet_id: PydanticObjectId, nurse_id: PydanticObjectId) -> ServiceSheetDetail:
        """
        Locks a patient in the triage queue and assigns them to a specific nurse.

        Validates the current state of the service sheet to prevent concurrent 
        triage attempts. Modifies the status to 'em_triagem_fase_1' and attaches 
        the nurse's unique ID.

        Args:
            sheet_id: The unique database ID of the service sheet.
            nurse_id: The unique database ID of the nurse initiating the triage.

        Returns:
            A populated ServiceSheetDetail DTO.

        Raises:
            ServiceSheetNotFoundError: If the sheet record does not exist.
            NurseNotFoundError: If the nurse ID is invalid.
            InvalidTriageStateError: If the patient is already in triage or finalized.
            PatientNotFoundError: If the associated patient record is missing.
        """
        
        sheet = await ServiceSheet.get(sheet_id)
        
        nurse = await User.get(nurse_id)
        
        if not sheet:
            raise ServiceSheetNotFoundError(f"Service sheet {sheet_id} not found.")
        
        if not nurse:
            raise NurseNotFoundError(f"Nurse {nurse_id} not found in the system.")
        
        if sheet.status != TriageStatus.aguardando_triagem:
            raise InvalidTriageStateError("Patient is currently in triage or already finished.")
        
        patient = await Patient.get(sheet.patient_ref)
        
        if not patient:
            raise PatientNotFoundError("Associated patient record not found.")
        
        await sheet.update(Set({
                    ServiceSheet.status: TriageStatus.em_triagem_fase_1,
                    ServiceSheet.nurse_ref: nurse_id
                }))
        
        return ServiceSheetDetail(
            id=sheet.id,
            patient=PatientCreate(**patient.model_dump()),
            status=TriageStatus.em_triagem_fase_1,
            nurse_ref=nurse_id,
            created_at=sheet.created_at,
            triage_data=sheet.triage_data,
            doctor_data=sheet.doctor_data
        )
    
    @staticmethod
    async def execute_phase_one(sheet_id: PydanticObjectId, input_data: TriageDataPhaseOne) -> List[TriageInvestigationQA]:
        """
        Executes Phase 1 of the triage process: Initial data and AI query generation.

        Stores the nurse's initial observations and patient vitals. Gathers clinical
        history and unit crowding context to orchestrate the MedGemma AI. Advances
        the state machine to Phase 2.

        Args:
            sheet_id: The unique database ID of the service sheet.
            input_data: A TriageDataPhaseOne schema containing vitals and initial notes.

        Returns:
            A list of generated TriageInvestigationQA objects containing the AI's questions.
            
        Raises:
            ServiceSheetNotFoundError: If the service sheet record does not exist.
        """
        
        sheet = await ServiceSheet.get(sheet_id)
        
        if not sheet:
            raise ServiceSheetNotFoundError(f"Service sheet {sheet_id} not found.")
        
        triage_data = TriageData(**input_data.model_dump())
        
        patient_history = await PatientService._get_patient_history_context(sheet.patient_ref)
        
        unity_history = await TriageService._calculate_unit_context()
        
        triage_questions = await MedGemmaProvider.orchestrate_investigation(triage_data=triage_data,
                                                                            patient_history=patient_history,
                                                                            unity_history=unity_history)
        
        triage_data.investigation_qa = triage_questions
        
        await sheet.update(Set({ServiceSheet.triage_data: triage_data,
                                ServiceSheet.status: TriageStatus.em_triagem_fase_2}))
        
        return triage_questions
    
    @staticmethod
    async def execute_phase_two(sheet_id: PydanticObjectId, input_data: TriageDataPhaseTwo) -> str:
        """
        Executes Phase 2 of the triage process: Patient responses and diagnostic suggestion.

        Receives the answers to the AI-generated questions from Phase 1. Reprocesses the 
        entire context through MedGemma to output a structured medical suggestion.

        Args:
            sheet_id: The unique database ID of the service sheet.
            input_data: A TriageDataPhaseTwo schema containing the answered questions. Advances
            the state machine to Phase 3.

        Returns:
            A string containing the AI-generated diagnostic hypothesis.
            
        Raises:
            ServiceSheetNotFoundError: If the sheet record does not exist.
            IncompleteTriageDataError: If Phase 1 data (vitals/observations) is missing.
        """
        
        sheet = await ServiceSheet.get(sheet_id)
        
        if not sheet:
            raise ServiceSheetNotFoundError(f"Service sheet {sheet_id} not found.")
        
        if not sheet.triage_data:
            raise IncompleteTriageDataError("Phase 1 data is missing. Cannot execute Phase 2.")
        
        triage_data = sheet.triage_data
        
        triage_data.investigation_qa = input_data.investigation_qa
        
        patient_history = await PatientService._get_patient_history_context(sheet.patient_ref)
        
        unity_history = await TriageService._calculate_unit_context()
        
        ai_observation = await MedGemmaProvider.generate_medical_suggestion(triage_data=triage_data, patient_history=patient_history, unity_history=unity_history)
        
        triage_data.ai_generated_sugestion = ai_observation
        
        await sheet.update(Set({ServiceSheet.triage_data: triage_data,
                                ServiceSheet.status: TriageStatus.em_triagem_fase_3}))
        
        return ai_observation
    
    @staticmethod
    async def execute_phase_three(sheet_id: PydanticObjectId, input_data: TriageDataPhaseThree) -> bool:
        """
        Executes Phase 3 of the triage process: Final risk classification.

        Records the final clinical risk level and nurse notes. Advances the patient's 
        status to the medical waiting queue and triggers a non-blocking background 
        task to generate the summarized doctor's briefing via LLM.

        Args:
            sheet_id: The unique database ID of the service sheet.
            input_data: A TriageDataPhaseThree schema containing the final risk assessment.

        Returns:
            True upon successful completion and background task dispatch.
            
        Raises:
            ServiceSheetNotFoundError: If the sheet record does not exist.
            IncompleteTriageDataError: If prior phase data is missing.
        """
        
        sheet = await ServiceSheet.get(sheet_id)
        
        if not sheet:
            raise ServiceSheetNotFoundError(f"Service sheet {sheet_id} not found.")
            
        if not sheet.triage_data:
            raise IncompleteTriageDataError("Previous triage data is missing. Cannot finalize Phase 3.")
        
        triage_data = sheet.triage_data
        
        update_dict = input_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(triage_data, key, value)
        
        await sheet.update(Set({
            ServiceSheet.triage_data: triage_data,
            ServiceSheet.status: TriageStatus.aguardando_medico
        }))
        
        asyncio.create_task(MedGemmaProvider.generate_doctor_summary(sheet))
        
        return True

    @staticmethod
    async def get_triage_session(sheet_id: PydanticObjectId) -> ServiceSheetDetail:
        """
        Retrieves the exact current state of a triage session.

        Allows the frontend to recover the triage form at the exact phase 
        it was interrupted (e.g., during page reloads or network drops).

        Args:
            sheet_id: The unique database ID of the service sheet.

        Returns:
            A populated ServiceSheetDetail DTO containing the current status and partial data.

        Raises:
            ServiceSheetNotFoundError: If the sheet record does not exist.
            PatientNotFoundError: if the patient record does not exist.
        """
        sheet = await ServiceSheet.get(sheet_id)
        if not sheet:
            raise ServiceSheetNotFoundError(f"Service sheet {sheet_id} not found.")
            
        patient = await Patient.get(sheet.patient_ref)
        if not patient:
            raise PatientNotFoundError("Associated patient record not found.")

        return ServiceSheetDetail(
            id=sheet.id,
            patient=PatientCreate(**patient.model_dump()),
            status=sheet.status,
            nurse_ref=sheet.nurse_ref,
            created_at=sheet.created_at,
            triage_data=sheet.triage_data,
            doctor_data=sheet.doctor_data
        )