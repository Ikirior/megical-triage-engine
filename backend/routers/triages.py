from fastapi import APIRouter, HTTPException, Depends
from http import HTTPStatus
from typing import List
from beanie import PydanticObjectId

from contracts import (
    TriageQueueItem, ServiceSheetDetail, 
    TriageInvestigationQA, TriageDataPhaseOne, 
    TriageDataPhaseTwo, TriageDataPhaseThree
)
from models import User
from dependencies import get_current_nurse_user
from services.triages import TriageService
from exceptions import (
    ServiceSheetNotFoundError, NurseNotFoundError, 
    PatientNotFoundError, InvalidTriageStateError, 
    IncompleteTriageDataError,
)

router = APIRouter(prefix="/triages", tags=["triage_management"])

@router.get("/queue", response_model=List[TriageQueueItem])
async def get_triage_queue(current_nurse: User = Depends(get_current_nurse_user)):
    """
    Retrieves the queue of patients waiting for triage.

    Args:
        current_nurse: The authenticated nurse or admin, injected by dependency.

    Returns:
        A list of TriageQueueItem objects representing patients awaiting service.
    """
    
    queue = await TriageService.get_triage_queue(nurse_id=current_nurse.id)
    return queue

@router.post("/{sheet_id}/start", response_model=ServiceSheetDetail)
async def start_triage(sheet_id: PydanticObjectId, current_nurse: User = Depends(get_current_nurse_user)):
    """
    Locks a service sheet and assigns it to the requesting nurse.

    The nurse ID is securely extracted from the authenticated user's token.

    Args:
        sheet_id: The unique PydanticObjectId of the service sheet.
        current_nurse: The authenticated nurse or admin, injected by dependency.

    Returns:
        The updated ServiceSheetDetail object reflecting the 'em_triagem' status.

    Raises:
        HTTPException: If the sheet/patient is not found (404) or if the state is invalid (400).
    """
    
    try:
        sheet_detail = await TriageService.start_triage(sheet_id=sheet_id,
                                                        nurse_id=current_nurse.id)
        return sheet_detail
    
    except(ServiceSheetNotFoundError, NurseNotFoundError, PatientNotFoundError) as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=str(e))
    
    except InvalidTriageStateError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e))

@router.post("/{sheet_id}/phase-one", response_model=List[TriageInvestigationQA])
async def execute_part_one(sheet_id: PydanticObjectId, input_data: TriageDataPhaseOne, current_nurse: User = Depends(get_current_nurse_user)):
    """
    Executes Phase 1 of triage, saving vitals and fetching AI questions.

    Args:
        sheet_id: The unique PydanticObjectId of the service sheet.
        input_data: A TriageDataPhaseOne schema containing vitals and initial observations.
        current_nurse: The authenticated nurse or admin, injected by dependency.

    Returns:
        A list of AI-generated TriageInvestigationQA objects for the nurse to ask.

    Raises:
        HTTPException: If the sheet is not found (404).
    """
    
    try:
        questions = await TriageService.execute_phase_one(sheet_id=sheet_id,
                                                          input_data=input_data)
        return questions
    
    except ServiceSheetNotFoundError as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=str(e))

@router.post("/{sheet_id}/phase-two", response_model=str)
async def execute_part_two(sheet_id: PydanticObjectId, input_data: TriageDataPhaseTwo, current_nurse: User = Depends(get_current_nurse_user)):
    """
    Executes Phase 2 of triage, processing patient answers to generate a diagnostic suggestion.

    Args:
        sheet_id: The unique PydanticObjectId of the service sheet.
        input_data: A TriageDataPhaseTwo schema containing answered questions.
        current_nurse: The authenticated nurse or admin, injected by dependency.

    Returns:
        The AI-generated medical suggestion string.

    Raises:
        HTTPException: If the sheet is not found (404) or Phase 1 data is missing (400).
    """
    
    try:
        suggestion = await TriageService.execute_phase_two(sheet_id=sheet_id,
                                                          input_data=input_data)
        return suggestion
    
    except ServiceSheetNotFoundError as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=str(e))
        
    except IncompleteTriageDataError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e))

@router.post("/{sheet_id}/phase-three", response_model=bool)
async def execute_part_three(sheet_id: PydanticObjectId, input_data: TriageDataPhaseThree, current_nurse: User = Depends(get_current_nurse_user)):
    """
    Executes Phase 3, finalizing the triage and assigning the clinical risk.

    Args:
        sheet_id: The unique PydanticObjectId of the service sheet.
        input_data: A TriageDataPhaseThree schema containing the final risk level.
        current_nurse: The authenticated nurse or admin, injected by dependency.

    Returns:
        A boolean confirming the operation success and trigger of the background task.

    Raises:
        HTTPException: If the sheet is not found (404) or prior phase data is missing (400).
    """
    
    try:
        success = await TriageService.execute_phase_three(sheet_id=sheet_id, input_data=input_data)
        return success
    
    except ServiceSheetNotFoundError as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=str(e))
    
    except IncompleteTriageDataError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{sheet_id}/session", response_model=ServiceSheetDetail)
async def get_triage_session(sheet_id: PydanticObjectId, current_nurse: User = Depends(get_current_nurse_user)):
    """
    Retrieves the current state of an active triage session for state recovery.

    Provides the frontend with the exact phase and partial data of a triage 
    in progress, preventing data loss during page reloads. Enforces strict 
    authorization to prevent Insecure Direct Object Reference (IDOR) vulnerabilities.

    Args:
        sheet_id: The unique PydanticObjectId of the service sheet to recover.
        current_nurse: The authenticated nurse, injected by dependency.

    Returns:
        The requested ServiceSheetDetail document containing the current status
        and any saved triage data.

    Raises:
        HTTPException: If the session belongs to a different nurse (HTTP 401),
                       if the service sheet is not found (HTTP 404), or if the
                       associated patient is not found (HTTP 404).
    """
    
    try:
        session_data = await TriageService.get_triage_session(sheet_id=sheet_id)
        
        if session_data.nurse_ref != current_nurse.id:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Nurse trying to access data that he does not have access to."
            )
        
        return session_data
    
    except ServiceSheetNotFoundError as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=str(e)
        )
    except PatientNotFoundError as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=str(e)
        )