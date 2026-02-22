from fastapi import APIRouter, HTTPException, Depends, Request
from http import HTTPStatus
from typing import Optional
from datetime import datetime, date
from beanie import PydanticObjectId

from contracts import PatientCreate, PatientUpdate, RaceEnum, SexEnum, ServiceSheetResponse
from models import Patient, ServiceSheet, User
from dependencies import get_current_receptionist_user
from services.patients import PatientService
from exceptions import PatientNotFoundError, ReceptionistNotFoundError, DuplicatePatientError

router = APIRouter(prefix="/patients", tags=["patient_management"])

@router.get("/{cpf}", response_model = Optional[Patient])
async def get_patient(cpf: str, current_receptionist: User = Depends(get_current_receptionist_user)):
    """
    Retrieves a patient's demographic record by their unique CPF.

    Args:
        cpf: The unique brazilian identification string of the target patient.
        current_receptionist: The authenticated receptionist, injected by dependency.

    Returns:
        The requested Patient document object.

    Raises:
        HTTPException: If the patient CPF does not exist in the database (HTTP 404).
    """
    
    try:
        patient = await PatientService.get_patient_by_cpf(cpf)
        return patient

    except PatientNotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Incorrect patient CPF or patient does not exist in the database."
        )
    


@router.post("/", response_model = Patient, status_code= HTTPStatus.CREATED)
async def create_patient(patient_data: PatientCreate, current_receptionist: User = Depends(get_current_receptionist_user)):
    """
    Registers a new patient in the system demographics.

    Args:
        patient_data: A PatientCreate schema containing the initial demographic data.
        current_receptionist: The authenticated receptionist, injected by dependency.

    Returns:
        The newly created Patient document object.

    Raises:
        HTTPException: If a patient with the provided CPF already exists (HTTP 409).
    """
    
    try:
        new_patient = await PatientService.create_patient(patient_data)
        return new_patient
    
    except DuplicatePatientError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Patient with this CPF already exists."
        )

@router.put("/{patient_id}", response_model = Patient)
async def update_patient(patient_id: PydanticObjectId, request: Request, current_receptionist: User = Depends(get_current_receptionist_user)):
    """
    Updates specific demographic fields of an existing patient.

    Args:
        patient_id: The unique PydanticObjectId of the patient to update.
        patient_data: A PatientUpdate schema containing the modified fields.
        current_receptionist: The authenticated receptionist, injected by dependency.

    Returns:
        The updated Patient document object.

    Raises:
        HTTPException: If invalid fields are sent (HTTP 400) or if the patient ID does not exist (HTTP 404).
    """
    
    payload = await request.json()
    allowed_fields = {"address", "companion", "phone_num", "sex"}
    invalid_fields = [key for key in payload.keys() if key not in allowed_fields]
    
    if invalid_fields:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Update failed. Unauthorized fields detected: {', '.join(invalid_fields)}"
        )
    
    patient_data = PatientUpdate(**payload)
    
    try:
        updated_patient = await PatientService.update_patient(patient_id=patient_id, new_data=patient_data)
        return updated_patient
    
    except PatientNotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Incorrect patient ID or patient does not exist in the database."
            )

@router.post("/{patient_id}/triage", response_model= ServiceSheetResponse, status_code= HTTPStatus.CREATED)
async def check_in_patient(patient_id: PydanticObjectId, current_receptionist: User = Depends(get_current_receptionist_user)):
    """
    Checks a patient into the triage queue.

    Initiates the clinical flow by creating a ServiceSheet. The receptionist ID 
    is automatically extracted from the authenticated user token to guarantee data integrity.

    Args:
        patient_id: The unique PydanticObjectId of the patient entering the queue.
        current_receptionist: The authenticated receptionist, injected by dependency.

    Returns:
        The newly created ServiceSheet document formatted as a ServiceSheetResponse DTO.

    Raises:
        HTTPException: If the patient ID or receptionist ID does not exist (HTTP 404).
    """
    
    try:
        new_service = await PatientService.check_in_patient(patient_id=patient_id,
                                                            receptionist_id=current_receptionist.id)
        return new_service
    
    except PatientNotFoundError as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Incorrect patient ID or patient does not exist in the database."
            )
    
    except ReceptionistNotFoundError as e:
        raise  HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Incorrect receptionist ID or receptionist does not exist in the database."
            )