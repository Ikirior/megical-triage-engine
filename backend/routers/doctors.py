from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime, timedelta, date
from beanie import PydanticObjectId

# Imports dos Contratos
from contracts import (
    DoctorQueueItem, ServiceSheetDetail, DoctorData,
    TriageStatus, PatientCreate, RaceEnum, SexEnum,
    TriageData, Vitals, TriageInvestigationQA, UnityContextSnapshot
)

router = APIRouter(prefix="/doctors", tags=["doctor_management"])

@router.get("/queue", response_model= List[DoctorQueueItem])
async def get_doctor_queue():
    
    return [
        DoctorQueueItem(
            id=PydanticObjectId(),
            patient_name="Sr. José",
            risk_classification="vermelho", # Prioridade 1
            waiting_time_minutes=45,
            waiting_since=datetime.now() - timedelta(minutes=45)
        ),
        DoctorQueueItem(
            id=PydanticObjectId(),
            patient_name="Maria da Silva",
            risk_classification="laranja", # Prioridade 2
            waiting_time_minutes=15,
            waiting_since=datetime.now() - timedelta(minutes=15)
        ),
        DoctorQueueItem(
            id=PydanticObjectId(),
            patient_name="João Souza",
            risk_classification="verde", # Prioridade 3
            waiting_time_minutes=120, 
            waiting_since=datetime.now() - timedelta(minutes=120)
        )
    ]

@router.post("/{sheet_id}/start", response_model=ServiceSheetDetail)
async def start_consultation(sheet_id: PydanticObjectId, doctor_id: PydanticObjectId):
    patient_mock = PatientCreate(
            name="Maria da Silva",
            cpf="123.456.789-00",
            rg="12.345.678-9",
            birth_date=date(1980, 5, 20),
            address="Rua Mock, 123",
            companion=False,
            race=RaceEnum.parda,
            sex=SexEnum.feminino,
            phone_num="22999999999"
        )
    triage_data_mock = TriageData(
        vitals=Vitals(
            systolic_bp=180, 
            diastolic_bp=110,
            heart_rate=90,
            temperature=36.5,
            oxygen_saturation=96
        ),
        nurse_initial_observations="Paciente relata cefaleia intensa na região occipital e tontura.",
        
        investigation_qa=[
            TriageInvestigationQA(
                question_id=PydanticObjectId(),
                question_text="O paciente suspendeu medicação de uso contínuo?",
                ai_reasoning="Pico hipertensivo pode indicar má adesão.",
                patient_answer="Sim, acabou o Losartana faz 3 dias."
            )
        ],
        
        ai_generated_sugestion="- Crise Hipertensiva por rebote/má adesão. Risco de AVC descartado preliminarmente (sem déficit motor).",
        
        risk_classification="laranja",
        final_nurse_notes="Paciente orientada a aguardar sentada. Nega dor no peito."
    )
    
    return ServiceSheetDetail(
        id=sheet_id,
        patient=patient_mock,
        status=TriageStatus.aguardando_medico,
        created_at=datetime.now() - timedelta(minutes=30),
        
        triage_data=triage_data_mock, 
        
        doctor_data=None 
    )

@router.post("/{sheet_id}/finish", response_model=bool)
async def finish_consultation(sheet_id: PydanticObjectId, input_data: DoctorData):
    
    return True