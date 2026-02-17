from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from datetime import datetime, date, timedelta
from typing import List, Optional, Literal
from beanie import PydanticObjectId

class RaceEnum(str, Enum):
    branca = "branca"
    preta = "preta"
    parda = "parda"
    amarela = "amarela"
    indigena = "indigena"
    ignorado = "ignorado"

class SexEnum(str, Enum):
    masculino = "M"
    feminino = "F"
    outro = "outro"

class TriageStatus(str, Enum):
    aguardando_triagem = "aguardando_triagem"
    em_triagem = "em_triagem"
    aguardando_medico = "aguardando_medico"
    finalizado = "finalizado"

class UserBase(BaseModel):
    name: str
    email: EmailStr
    cpf: str
    rg: str
    role: Literal["receptionist", "nurse", "doctor", "admin"]
    specialization: Optional[str] = None

# Substitui as classes BasicWorkerSchema e SpecializedWorkerSchema
class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    specialization: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: PydanticObjectId
    created_at: datetime

class PatientCreate(BaseModel):
    name: str
    cpf: str
    rg: str
    birth_date: date
    address: str
    companion: bool
    race: RaceEnum
    sex: SexEnum
    phone_num: str

class PatientUpdate(BaseModel):
    address: Optional[str] = None
    companion: Optional[bool] = None
    phone_num: Optional[str] = None
    sex: Optional[SexEnum] = None

class PatientHistoryItem(BaseModel):
    patient_id: PydanticObjectId
    created_at: datetime
    triage_data: Optional[TriageData] = None
    doctor_data: Optional[DoctorData] = None

class Vitals(BaseModel):
    systolic_bp: int = Field(..., description = "Pressão Sistólica (ex: 120)")
    diastolic_bp: int = Field(..., description = "Pressão Diastólica (ex: 80)")
    heart_rate: int = Field(..., description = "Batimentos por minuto")
    temperature: float = Field(..., description = "Temperatura em Celsius" )
    oxygen_saturation: float = Field(..., ge=0, le=100, description ="Saturação O2 %")
    extras: Optional[dict] = None

class TriageInvestigationQA(BaseModel):
    question_id: PydanticObjectId
    question_text: str
    ai_reasoning: str
    patient_answer: Optional[str] = None

class UnityContextSnapshot(BaseModel):
    captured_at: datetime
    # Removido o available_resources
    crowding_level: Literal["low", "medium", "high", "critial"]

class TriageDataPhaseOne(BaseModel):
    vitals: Vitals
    nurse_initial_observations: str

class TriageDataPhaseTwo(BaseModel):
    investigation_qa: List[TriageInvestigationQA] = []

class TriageDataPhaseThree(BaseModel):
    ai_generated_sugestion: Optional[str] = None
    risk_classification: Optional[Literal["azul", "verde", "amarelo", "laranja", "vermelho"]] = None
    final_nurse_notes: Optional[str] = None

class TriageQueueItem(BaseModel):
    sheet_id: PydanticObjectId
    patient_id: PydanticObjectId
    patient_name: str
    arrival_time: datetime

class DoctorQueueItem(BaseModel):
    id: PydanticObjectId
    patient_name: str
    risk_classification: Literal["azul", "verde", "amarelo", "laranja", "vermelho"]
    waiting_time_minutes: int
    waiting_since: datetime

class TriageData(BaseModel):
    # Fase 1
    vitals: Vitals
    nurse_initial_observations: str
    
    # Fase 2
    unit_snapshot: Optional[UnityContextSnapshot] = None
    investigation_qa: List[TriageInvestigationQA] = []
    
    # Fase 3
    ai_generated_sugestion: Optional[str] = None
    risk_classification: Optional[Literal["azul", "verde", "amarelo", "laranja", "vermelho"]] = None
    final_nurse_notes: Optional[str] = None

class DoctorData(BaseModel):
    ai_pre_consultation_summary: Optional[str] = None
    doctor_notes:str
    diagnosis_cid: Optional[str] = None
    prescription: Optional[str] = None

class DoctorQueueItem(BaseModel):
    id: PydanticObjectId
    patient_name: str
    risk_classification: Literal["azul", "verde", "amarelo", "laranja", "vermelho"]
    waiting_time_minutes: int

class ServiceSheetResponse(BaseModel):
    id : PydanticObjectId
    patient_ref: PydanticObjectId
    receptionist_ref: PydanticObjectId
    status: TriageStatus = TriageStatus.aguardando_triagem
    created_at: datetime

class ServiceSheetDetail(BaseModel):
    id: PydanticObjectId
    patient: PatientCreate
    status: TriageStatus
    created_at: datetime
    triage_data: Optional[TriageData] = None
    doctor_data: Optional[DoctorData] = None