from beanie import PydanticObjectId
from typing import Optional, List
from models import Patient, ServiceSheet, User
from contracts import (PatientCreate,PatientUpdate, PatientHistoryItem, TriageStatus)
from exceptions import PatientNotFoundError, ReceptionistNotFoundError, DuplicatePatientError

class PatientService:
    """
    Manages the patient lifecycle and reception check-in processes.

    This service encapsulates the business logic for patient registration,
    demographic updates, context retrieval for the MedGemma AI, and the 
    initial triage queue entry.

    Note:
        All database operations are asynchronous and utilize the Beanie ODM.
    """ 
    
    @staticmethod
    async def get_patient_by_cpf(cpf: str) -> Patient:
        """
        Retrieves a patient record using their unique CPF.

        Used by the reception to verify if a patient is already registered
        in the system before initiating a new check-in or registration process.

        Args:
            cpf: The patient's unique identification string (Brazilian CPF).

        Returns:
            The Patient document if found, or None to signal the need for a new registration.
        """
        
        find_patient = await Patient.find_one(Patient.cpf == cpf)
        
        if not find_patient:
            raise PatientNotFoundError("Incorrect patient CPF or patient does not exist in the database.")
        
        return find_patient
    
    @staticmethod
    async def create_patient(data: PatientCreate) -> Patient:
        """
        Creates a new demographic record for a patient.

        Persists the initial patient data into the database. CPF uniqueness
        is enforced by the database index defined in the Patient model.

        Args:
            data: A PatientCreate schema containing the initial demographic data.

        Returns:
            The newly created Patient document.
        """
        existing_patient = await Patient.find_one(Patient.cpf == data.cpf)
        
        if existing_patient:
            raise DuplicatePatientError("Patient with this CPF already exists.")
        
        new_patient = Patient(**data.model_dump())
        
        await new_patient.save()
        
        return new_patient
    
    @staticmethod
    async def update_patient(patient_id: PydanticObjectId, new_data: PatientUpdate) -> Patient:
        """
        Updates specific demographic or contact fields of an existing patient.

        Applies partial updates (e.g., changing address or phone number) 
        without overwriting unmodified fields.

        Args:
            patient_id: The unique database ID of the patient.
            new_data: A PatientUpdate schema containing only the fields to modify.

        Returns:
            The updated Patient document, or None if the patient is not found.
        """
        
        patient = await Patient.get(patient_id)
        
        if not patient:
            raise PatientNotFoundError("Incorrect patient CPF or patient does not exist in the database.")

        update_dict = new_data.model_dump(exclude_unset=True)
        
        for key, value in update_dict.items():
            setattr(patient, key, value)
        
        await patient.save()
        
        return patient
    
    @staticmethod
    async def _get_patient_history_context(patient_id: PydanticObjectId) -> List[PatientHistoryItem]:
        """
        Retrieves the clinical history context for the MedGemma LLM.

        Fetches the 5 most recent finalized service sheets for a given patient.
        This simplified historical data is injected into the LLM prompt to 
        provide longitudinal context for the triage decision.

        Args:
            patient_id: The unique database ID of the patient.

        Returns:
            A list of PatientHistoryItem DTOs sorted by creation date (newest first).
        """
        sheets = await ServiceSheet.find(
            ServiceSheet.patient_ref == patient_id,
            ServiceSheet.status == TriageStatus.finalizado
        ).sort(-ServiceSheet.created_at).limit(5).to_list()
        
        history_items = []
        
        for sheet in sheets:
            
            history_items.append(PatientHistoryItem(patient_id=sheet.patient_ref,
                                                    created_at=sheet.created_at,
                                                    triage_data=sheet.triage_data,
                                                    doctor_data=sheet.doctor_data))
        
        return history_items

    @staticmethod
    async def check_in_patient(patient_id: PydanticObjectId, receptionist_id: PydanticObjectId) -> ServiceSheet:
        """
        Initiates the triage process by placing a patient in the queue.

        Creates a new ServiceSheet with an initial waiting status. Medical
        data fields remain unpopulated at this stage.

        Args:
            patient_id: The unique database ID of the patient.
            receptionist_id: The unique database ID of the staff member performing the check-in.

        Returns:
            The newly created ServiceSheet document, or None if the patient or receptionist does not exist.
        """
        
        patient = await Patient.get(patient_id)
        if not patient:
            raise PatientNotFoundError("Incorrect patient CPF or patient does not exist in the database.")
        
        receptionist = await User.get(receptionist_id)
        if not receptionist:
            raise ReceptionistNotFoundError("Incorrect receptionist ID or receptionist does not exist in the database.")
        
        service_sheet = ServiceSheet(
            patient_ref=patient_id,
            receptionist_ref=receptionist_id,
            status=TriageStatus.aguardando_triagem
        )
        
        await service_sheet.insert()
        
        return service_sheet