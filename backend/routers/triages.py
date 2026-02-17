from fastapi import APIRouter, HTTPException
from http import HTTPStatus
from typing import Optional, List
from datetime import datetime, timedelta, date
from beanie import PydanticObjectId


from contracts import (TriageQueueItem, RaceEnum, SexEnum,
                       ServiceSheetResponse, ServiceSheetResponse, TriageStatus,
                       TriageInvestigationQA, TriageDataPhaseOne, TriageDataPhaseTwo,
                       TriageDataPhaseThree, ServiceSheetDetail, PatientCreate)
from models import Patient, ServiceSheet

router = APIRouter(prefix="/triages", tags=["triage_management"])

@router.get("/queue", response_model=List[TriageQueueItem])
async def get_triage_queue():
    """
    Retorna apenas o necessário para montar o Card no Front.
    """
    
    return [
        TriageQueueItem(
            sheet_id=PydanticObjectId(),
            patient_id=PydanticObjectId(),
            patient_name="Maria da Silva",
            arrival_time=datetime.now() - timedelta(minutes=25)
        ),
        TriageQueueItem(
            sheet_id=PydanticObjectId(),
            patient_id=PydanticObjectId(),
            patient_name="João Souza",
            arrival_time=datetime.now() - timedelta(minutes=10)
        )
    ]

@router.post("/{sheet_id}/start", response_model=ServiceSheetDetail)
async def start_triage(sheet_id: PydanticObjectId, nurse_id: PydanticObjectId):
    
    patient = PatientCreate(id=PydanticObjectId(),
                            name="Gabriel Lacerda",
                            cpf="123.456.789-00",
                            rg="12.345.678-9",
                            birth_date= date.today(),
                            address="Casa do Mock",
                            companion= False,
                            race= RaceEnum.ignorado,
                            sex=SexEnum.masculino,
                            phone_num="1234-5678")
    
    return ServiceSheetDetail(id=sheet_id,
                                patient=patient,
                                status=TriageStatus.em_triagem,
                                created_at=datetime.now())

@router.post("/{sheet_id}/phase-one", response_model=List[TriageInvestigationQA])
async def execute_part_one(sheet_id: PydanticObjectId, input_data: TriageDataPhaseOne):
    
    return [
        TriageInvestigationQA(question_id=PydanticObjectId(),
                            question_text="Isso é um mock somente para testar a API?",
                            ai_reasoning="Eu sou uma IA real?",
                            ),
        TriageInvestigationQA(question_id=PydanticObjectId(),
                            question_text="Isso é um mock somente para testar a API?",
                            ai_reasoning="Eu sou uma IA real?",
                            )
    ]

@router.post("/{sheet_id}/phase-two", response_model=str)
async def execute_part_two(sheet_id: PydanticObjectId, input_data: TriageDataPhaseTwo):
    
    return "Isso aqui é um exemplo de texto que pode ser retornado pela IA."

@router.post("/{sheet_id}/phase-three", response_model=bool)
async def execute_part_three(sheet_id: PydanticObjectId, input_data: TriageDataPhaseThree):
    
    return True