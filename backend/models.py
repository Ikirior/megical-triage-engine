from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Literal
from beanie import Document, PydanticObjectId

from contracts import UserBase, PatientCreate, TriageStatus, TriageData, DoctorData

class User(Document, UserBase):
    password_hash: str
    created_at: datetime = Field(default_factory = datetime.now)
    
    class Settings:
        name = "users"

# Used for Patient register
class Patient(Document, PatientCreate):
    medical_history_summary: Optional[str] = None
    
    class Settings:
        name = "patients"

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