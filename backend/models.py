from pydantic import Field
from datetime import datetime, date
from typing import Optional
from beanie import Document, Link, PydanticObjectId
from pymongo import IndexModel, ASCENDING

from contracts import UserBase, TriageStatus, TriageData, DoctorData, RaceEnum, SexEnum

class User(Document, UserBase):
    password_hash: str
    created_at: datetime = Field(default_factory = datetime.now)
    
    class Settings:
        name = "users"
        indexes = [
            IndexModel([("email", ASCENDING)]),
            IndexModel([("cpf", ASCENDING)], unique = True)
        ]

class Patient(Document):
    name: str
    cpf: str
    rg: str
    birth_date: date
    address: str
    companion: bool
    race: RaceEnum
    sex: SexEnum
    phone_num: str
    
    class Settings:
        name = "patients"
        
        indexes = [
            IndexModel([("cpf", ASCENDING)], unique = True)
        ]

class ServiceSheet(Document):
    patient_ref: PydanticObjectId
    receptionist_ref: PydanticObjectId
    status: TriageStatus = TriageStatus.aguardando_triagem
    nurse_ref: Optional[PydanticObjectId] = None
    doctor_ref: Optional[PydanticObjectId] = None
    
    created_at: datetime = Field(default_factory = datetime.now)
    updated_at: datetime = Field(default_factory = datetime.now)
    
    triage_data: Optional[TriageData] = None
    doctor_data: Optional[DoctorData] = None
    
    class Settings:
        name = "service_sheets"
        
        indexes = [
            IndexModel([("patient_ref", ASCENDING)]),
            IndexModel([("nurse_ref", ASCENDING)]),
            IndexModel([("doctor_ref", ASCENDING)]),
            # Index para filtragem por status e updated_at
            IndexModel([
                ("status", ASCENDING), 
                ("updated_at", ASCENDING)
            ]),
            # Index para filtrar por cor de risco e consulta na fila
            IndexModel([
                ("status", ASCENDING),
                ("triage_data.risk_classification", ASCENDING)
            ])
        ]