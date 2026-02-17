from fastapi import APIRouter, HTTPException
from http import HTTPStatus
from typing import Optional
from datetime import datetime, date
from beanie import PydanticObjectId

from contracts import PatientCreate, PatientUpdate, RaceEnum, SexEnum, ServiceSheetResponse
from models import Patient, ServiceSheet

router = APIRouter(prefix="/patients", tags=["patient_management"])

@router.get("/", response_model = Optional[Patient])
async def get_patient(cpf: str):
    
    patient_mock = Patient(id=PydanticObjectId(),
                        name="Gabriel Lacerda",
                        cpf=cpf,
                        rg="12.345.678-9",
                        birth_date= date.today(),
                        address="Casa do Mock",
                        companion= False,
                        race= RaceEnum.ignorado,
                        sex=SexEnum.masculino,
                        phone_num="1234-5678",
                        medical_history_summary= None)
    
    return None if cpf != "123.456.789-00" else patient_mock

@router.post("/", response_model = Patient, status_code= HTTPStatus.CREATED)
async def create_patient(patient_data: PatientCreate):
    
    return Patient(id= PydanticObjectId(),
                   **patient_data.model_dump())

@router.put("/{patient_id}", response_model = Patient)
async def update_patient(patient_id: PydanticObjectId, patient_data: PatientUpdate):
    
    pid = PydanticObjectId(patient_id) if PydanticObjectId.is_valid(patient_id) else PydanticObjectId()
    
    return Patient( id=pid,
                    name="Gabriel Lacerda",
                    cpf="123.456.789.00",
                    rg="12.345.678-9",
                    birth_date= date.today(),
                    address= patient_data.address or "Endereço Original",
                    companion= patient_data.companion if patient_data.companion is not None else False,
                    race = RaceEnum.ignorado,
                    sex= patient_data.sex or SexEnum.masculino,
                    phone_num= patient_data.phone_num or "22999999999",
                    medical_history_summary= None)

@router.post("/to-triage", response_model= ServiceSheetResponse, status_code= HTTPStatus.CREATED)
async def check_in_patient(patient_id: PydanticObjectId, receptionist_id: PydanticObjectId):
    
    pid = PydanticObjectId(patient_id) if PydanticObjectId.is_valid(patient_id) else PydanticObjectId()
    rid = PydanticObjectId(receptionist_id) if PydanticObjectId.is_valid(receptionist_id) else PydanticObjectId()
    
    return ServiceSheetResponse(id= PydanticObjectId(),
                                patient_ref= pid,
                                receptionist_ref= rid,
                                created_at= datetime.now(),
                                updated_at= datetime.now())