from fastapi import APIRouter, HTTPException
from http import HTTPStatus
from typing import List
from datetime import datetime
from beanie import PydanticObjectId

from models import User
from contracts import UserCreate, UserResponse, UserUpdate

def fake_hash_password(password: str):
    return f"hashed_{password}"

router = APIRouter(prefix = "/users",  tags=["user_management"])

@router.get("/", response_model=List[UserResponse])
async def list_users():
    """
    Retorna uma lista fixa de usuários para teste de layout.
    """
    return [
        UserResponse(
            id=PydanticObjectId(),
            name="Gabriel Lacerda",
            email="gabriel@medgemma.com.br",
            cpf="123.456.789-00",
            rg="12.345.678-9",
            role="admin",
            specialization=None,
            created_at=datetime.now()
        ),
        UserResponse(
            id=PydanticObjectId(),
            name="Dra. Ana Silva",
            email="ana@medgemma.com.br",
            cpf="987.654.321-00",
            rg="98.765.432-1",
            role="doctor",
            specialization="Cardiologia",
            created_at=datetime.now()
        )
    ]

@router.get("/{user_id}", response_model = UserResponse)
async def get_user(user_id: str):
    """
    Retorna sempre o mesmo usuário, fingindo que buscou pelo ID.
    """
    return UserResponse(
        id=PydanticObjectId(user_id) if PydanticObjectId.is_valid(user_id) else PydanticObjectId(),
        name="Usuário Mockado da Silva",
        email="mock@medgemma.com.br",
        cpf="000.000.000-00",
        rg="00.000.000-0",
        role="nurse",
        created_at=datetime.now()
    )

@router.post("/", response_model = UserResponse, status_code = HTTPStatus.CREATED)
async def create_user(user_data: UserCreate):
    """
    Recebe os dados, valida os tipos, e retorna como se tivesse criado.
    """
    
    return UserResponse(
        id=PydanticObjectId(),
        created_at=datetime.now(),
        **user_data.model_dump(exclude={"password"}) # Copia os dados enviados (menos senha)
    )

@router.put("/{user_id}", response_model = UserResponse)
async def update_user(user_id: str, user_data: UserUpdate):
    """
    Simula uma atualização de dados.
    """
    
    return UserResponse(
        id=PydanticObjectId(user_id) if PydanticObjectId.is_valid(user_id) else PydanticObjectId(),
        name=user_data.name or "Nome Não Alterado",
        email=user_data.email or "email@original.com",
        cpf="123.456.789-00",
        rg="12.345.678-9",
        role=user_data.role or "nurse",
        specialization=user_data.specialization,
        created_at=datetime.now()
    )

@router.delete("/{user_id}",status_code = HTTPStatus.NO_CONTENT)
async def delete_user(user_id: str):
    """
    Retorna 204 (No Content) para simular sucesso na remoção.
    """
    
    return None