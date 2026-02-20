from fastapi import APIRouter, HTTPException, Depends
from http import HTTPStatus
from typing import List
from beanie import PydanticObjectId

from contracts import DoctorQueueItem, ServiceSheetDetail, DoctorData
from models import User
from dependencies import get_current_doctor_user
from services.doctor import DoctorService
from exceptions import (
    ServiceSheetNotFoundError, DoctorNotFoundError, 
    PatientNotFoundError, InvalidConsultationStateError, 
    UnauthorizedDoctorError
)
router = APIRouter(prefix="/doctors", tags=["doctor_management"])

@router.get("/queue", response_model= List[DoctorQueueItem], )
async def get_doctor_queue(current_doctor: User = Depends(get_current_doctor_user)):
    """
    Retrieves the prioritized medical queue.

    Args:
        current_doctor: The authenticated doctor, injected by dependency.

    Returns:
        A list of patients waiting for medical consultation, sorted by risk.
    """
    
    queue = await DoctorService.get_doctor_queue()
    return queue

@router.post("/{sheet_id}/start", response_model=ServiceSheetDetail)
async def start_consultation(sheet_id: PydanticObjectId, current_doctor: User = Depends(get_current_doctor_user)):
    """
    Initiates a medical consultation by locking the service sheet.

    Args:
        sheet_id: The unique ID of the service sheet to start.
        current_doctor: The authenticated doctor, injected by dependency.

    Returns:
        The updated service sheet with 'em_atendimento' status.

    Raises:
        HTTPException 404: If sheet, doctor, or patient is not found.
        HTTPException 400: If the patient is already being attended.
    """
    
    try:
        sheet_detail = await DoctorService.start_consultation(
            sheet_id=sheet_id, 
            doctor_id=current_doctor.id
        )
        return sheet_detail
        
    except (ServiceSheetNotFoundError, DoctorNotFoundError, PatientNotFoundError) as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
    except InvalidConsultationStateError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))

@router.post("/{sheet_id}/finish", response_model=ServiceSheetDetail)
async def finish_consultation(sheet_id: PydanticObjectId, input_data: DoctorData, current_doctor: User = Depends(get_current_doctor_user)):
    """
    Finalizes the consultation and records clinical data.

    Args:
        sheet_id: The ID of the sheet to finalize.
        input_data: The diagnostic and prescription data.
        current_doctor: The authenticated doctor, injected by dependency.

    Returns:
        The finalized service sheet with 'finalizado' status.

    Raises:
        HTTPException 404: If sheet or patient is not found.
        HTTPException 400: If the consultation is not in progress.
        HTTPException 403: If another doctor tries to finish this sheet.
    """
    
    try:
        sheet_detail = await DoctorService.finish_consultation(
            sheet_id=sheet_id,
            doctor_id=current_doctor.id,
            input_data=input_data
        )
        return sheet_detail
        
    except (ServiceSheetNotFoundError, PatientNotFoundError) as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
    except InvalidConsultationStateError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    except UnauthorizedDoctorError as e:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=str(e))