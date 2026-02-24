from datetime import datetime
from typing import List
from beanie import PydanticObjectId
from beanie.operators import In, Set, Or, And

from models import ServiceSheet, Patient, User
from contracts import (
    DoctorQueueItem, ServiceSheetDetail, DoctorData, 
    TriageStatus, PatientCreate
)
from exceptions import (
    ServiceSheetNotFoundError, DoctorNotFoundError, 
    PatientNotFoundError, InvalidConsultationStateError, 
    UnauthorizedDoctorError
)

class DoctorService:
    """
    Manages the medical consultation workflow and the intelligent waiting queue.

    This service handles the retrieval of prioritized patient queues for doctors,
    the initiation of consultations (with concurrency locking), and the finalization
    of the medical service with the updated diagnostic data.
    """
    
    @staticmethod
    async def get_doctor_queue(doctor_id: PydanticObjectId) -> List[DoctorQueueItem]:
        """
        Retrieves the medical queue prioritized by clinical risk and waiting time.

        Fetches patients with the 'aguardando_medico' status. Prioritizes them first
        by their risk classification (vermelho > laranja > amarelo > verde > azul)
        and secondly by their waiting time in the unit. Uses batch fetching to 
        optimize database I/O.

        Returns:
            A list of DoctorQueueItem objects representing the sorted waiting queue.
        """
        
        sheets = await ServiceSheet.find(
            Or(
                ServiceSheet.status == TriageStatus.aguardando_medico,
                And(
                    ServiceSheet.doctor_ref == doctor_id,
                    ServiceSheet.status == TriageStatus.em_atendimento
                )
            )
        ).to_list()
        
        if not sheets:
            return []
        
        patient_ids = [sheet.patient_ref for sheet in sheets]
        
        patients = await Patient.find(In(Patient.id, patient_ids)).to_list()

        patient_map = {patient.id: patient.name for patient in patients}
        
        risk_weights = {
            "vermelho": 1,
            "laranja": 2,
            "amarelo": 3,
            "verde": 4,
            "azul": 5
        }
        
        queue = []
        now = datetime.now()

        for sheet in sheets:
            wait_time = int((now - sheet.created_at).total_seconds() / 60)
            
            risk = sheet.triage_data.risk_classification if sheet.triage_data and sheet.triage_data.risk_classification else "azul"
            
            queue.append(DoctorQueueItem(
                sheet_id=sheet.id,
                patient_id=sheet.patient_ref,
                patient_name=patient_map.get(sheet.patient_ref, "Unknown"),
                risk_classification=risk,
                status=sheet.status,
                waiting_since=sheet.created_at
            ))
        
        queue.sort(key=lambda x: (risk_weights.get(x.risk_classification, 5), x.waiting_since))
        
        return queue
    
    @staticmethod
    async def start_consultation(sheet_id: PydanticObjectId, doctor_id: PydanticObjectId) -> ServiceSheetDetail:
        """
        Locks a patient for a specific doctor, preventing concurrent access.

        Validates the patient's availability and assigns them to the requesting doctor,
        changing the status to 'em_atendimento'.

        Args:
            sheet_id: The unique database ID of the service sheet.
            doctor_id: The unique database ID of the doctor starting the consultation.

        Returns:
            A populated ServiceSheetDetail DTO, or None if the sheet or doctor is missing.

        Raises:
            HTTPException: If the patient is not available (400) or record not found (404).
        """
        
        sheet = await ServiceSheet.get(sheet_id)
        
        if not sheet:
            raise ServiceSheetNotFoundError(f"Service sheet {sheet_id} not found.")
        
        doctor = await User.get(doctor_id)

        if not doctor:
            raise DoctorNotFoundError(f"Doctor {doctor_id} not found in the system.")
        
        if sheet.status != TriageStatus.aguardando_medico:
            raise InvalidConsultationStateError("Patient is not available for consultation or already taken.")
        
        patient = await Patient.get(sheet.patient_ref)
        if not patient:
            raise PatientNotFoundError("Patient record not found.")
        
        temp_doctor_data = DoctorData(ai_pre_consultation_summary="batata doce, doce, doce, doce, doce")
        
        await sheet.update(Set({
            ServiceSheet.status: TriageStatus.em_atendimento,
            ServiceSheet.doctor_ref: doctor_id,
            ServiceSheet.doctor_data: temp_doctor_data # Temporary
        }))
        
        return ServiceSheetDetail(
            id=sheet.id,
            patient=PatientCreate(**patient.model_dump()),
            nurse_ref=sheet.nurse_ref,
            status=TriageStatus.em_atendimento,
            created_at=sheet.created_at,
            triage_data=sheet.triage_data,
            doctor_data=sheet.doctor_data
        )
    
    @staticmethod
    async def finish_consultation(sheet_id: PydanticObjectId, doctor_id: PydanticObjectId, input_data: DoctorData) -> ServiceSheetDetail:
        """
        Finalizes the medical service, updating the diagnostic logic and releasing the patient.

        Records the doctor's final diagnosis, notes, and prescription. Ensures that only
        the assigned doctor can finish the consultation and updates the status to 'finalizado'.

        Args:
            sheet_id: The unique database ID of the service sheet.
            doctor_id: The unique database ID of the assigned doctor.
            input_data: A DoctorData schema containing the final medical input.

        Returns:
            A populated ServiceSheetDetail DTO with the updated data, or None if the sheet is missing.

        Raises:
            HTTPException: If the doctor is not assigned (403), consultation is not active (400),
                            or the patient record is missing (404).
        """
        
        sheet = await ServiceSheet.get(sheet_id)
        
        if not sheet:
            raise ServiceSheetNotFoundError(f"Service sheet {sheet_id} not found.")
        
        if sheet.doctor_ref != doctor_id:
            raise UnauthorizedDoctorError("Only the assigned doctor can finish this consultation.")
        
        if sheet.status != TriageStatus.em_atendimento:
            raise InvalidConsultationStateError("Consultation is not in progress.")
        
        patient = await Patient.get(sheet.patient_ref)
        
        if not patient:
            raise PatientNotFoundError("Patient record not found.")
        
        await sheet.update(Set({
            ServiceSheet.doctor_data: input_data,
            ServiceSheet.status: TriageStatus.finalizado
        }))
        
        return ServiceSheetDetail(
            id=sheet.id,
            patient=PatientCreate(**patient.model_dump()),
            nurse_ref=sheet.nurse_ref,
            status=TriageStatus.finalizado,
            created_at=sheet.created_at,
            triage_data=sheet.triage_data,
            doctor_data=input_data
        )

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
            doctor_ref=sheet.doctor_ref,
            created_at=sheet.created_at,
            triage_data=sheet.triage_data,
            doctor_data=sheet.doctor_data
        )