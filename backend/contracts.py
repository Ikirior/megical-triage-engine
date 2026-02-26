from __future__ import annotations
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
    em_triagem_fase_1 = "em_triagem_fase_1"
    em_triagem_fase_2 = "em_triagem_fase_2"
    em_triagem_fase_3 = "em_triagem_fase_3"
    aguardando_medico = "aguardando_medico"
    em_atendimento = "em_atendimento"
    finalizado = "finalizado"

class UserBase(BaseModel):
    name: str
    email: EmailStr
    cpf: str
    rg: str
    role: Literal["receptionist", "nurse", "doctor", "admin"]
    specialization: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
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
    crowding_level: Literal["low", "medium", "high", "critical"]

class TriageDataPhaseOne(BaseModel):
    vitals: Vitals
    nurse_initial_observations: str

class TriageDataPhaseTwo(BaseModel):
    investigation_qa: List[TriageInvestigationQA] = []

class TriageDataPhaseThree(BaseModel):
    ai_generated_suggestion: Optional[str] = None
    risk_classification: Optional[Literal["azul", "verde", "amarelo", "laranja", "vermelho"]] = None
    final_nurse_notes: Optional[str] = None

class TriageQueueItem(BaseModel):
    sheet_id: PydanticObjectId
    patient_id: PydanticObjectId
    patient_name: str
    arrival_time: datetime
    status: TriageStatus

class DoctorQueueItem(BaseModel):
    sheet_id: PydanticObjectId
    patient_id: PydanticObjectId
    patient_name: str
    risk_classification: Literal["azul", "verde", "amarelo", "laranja", "vermelho"]
    status: TriageStatus
    waiting_since: datetime

class TriageData(BaseModel):
    # Phase 1
    vitals: Vitals
    nurse_initial_observations: str
    
    # Phase 2
    investigation_qa: List[TriageInvestigationQA] = []
    
    # Phase 3
    ai_generated_suggestion: Optional[str] = None
    risk_classification: Optional[Literal["azul", "verde", "amarelo", "laranja", "vermelho"]] = None
    final_nurse_notes: Optional[str] = None

class DoctorData(BaseModel):
    ai_pre_consultation_summary: Optional[str] = None
    doctor_notes: Optional[str] = None
    diagnosis_cid: Optional[str] = None
    prescription: Optional[str] = None

class ServiceSheetResponse(BaseModel):
    id : PydanticObjectId
    patient_ref: PydanticObjectId
    receptionist_ref: PydanticObjectId
    status: TriageStatus = TriageStatus.aguardando_triagem
    created_at: datetime

class ServiceSheetDetail(BaseModel):
    id: PydanticObjectId
    patient: PatientCreate
    nurse_ref: PydanticObjectId
    doctor_ref: Optional[PydanticObjectId] = None
    status: TriageStatus
    created_at: datetime
    triage_data: Optional[TriageData] = None
    doctor_data: Optional[DoctorData] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class GeneratedQuestion(BaseModel):
    question_text: str = Field(description="A clear question in Portuguese for the patient.")
    historical_reference: Optional[str] = Field(description="Exact citation of the historical data (e.g., 'CID', 'Date', 'Pains', etc.) that prompted the question. Use 'N/A' if based only on current data.")
    ai_reasoning: str = Field(description="Clinical rationale based on risks.")

class InvestigationDecision(BaseModel):
    needs_investigation: bool = Field(description="True if the case requires additional questions for screening.")
    reasoning: str = Field(description="Technical analysis of the case comparing historical data with the current data entry.")
    num_questions_decided: int = Field(description="The number of questions was decided based on their criticality and gaps in the historical record.")
    questions: List[GeneratedQuestion] = Field(default_factory=list)

class ClinicalSuggestion(BaseModel):
    risk_color: Literal["azul", "verde", "amarelo", "laranja", "vermelho"] = Field(description="Risk classification according to the standard 5-level clinical severity guidelines")
    technical_summary: str = Field(description="Clinical summary in bullet points for nursing.")
    observation_points: List[str] = Field(description="Specific warning signs for the doctor.")

class PatientHistoryItem(BaseModel):
    patient_id: PydanticObjectId
    created_at: datetime
    triage_data: Optional[TriageData] = None
    doctor_data: Optional[DoctorData] = None
