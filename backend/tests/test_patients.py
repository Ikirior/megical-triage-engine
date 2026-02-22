import pytest
from http import HTTPStatus
from beanie import PydanticObjectId

@pytest.mark.asyncio
async def test_receptionist_can_create_patient(receptionist_client):
    """
    Verifies that an authorized receptionist can register a new patient.
    """
    patient_payload = {
        "name": "Maria Silva",
        "cpf": "111.222.333-44",
        "rg": "RJ-99.888",
        "birth_date": "1990-05-15",
        "address": "Rua Exemplo, 123",
        "companion": True,
        "race": "parda",
        "sex": "F",
        "phone_num": "(11) 98765-4321"
    }

    response = await receptionist_client.post("/patients/", json=patient_payload)
    
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["cpf"] == "111.222.333-44"
    assert data["companion"] is True
    assert "_id" in data

@pytest.mark.asyncio
async def test_create_patient_conflict_duplicate_cpf(receptionist_client, seed_patient):
    """
    Ensures the system rejects patient registrations with duplicate CPFs.
    """
    duplicate_payload = {
        "name": "Clone Patient",
        "cpf": seed_patient.cpf,
        "rg": "SP-11.222",
        "birth_date": "1980-01-01",
        "address": "Outra Rua, 44",
        "companion": False,
        "race": "branca",
        "sex": "M",
        "phone_num": "(22) 11111-2222"
    }

    response = await receptionist_client.post("/patients/", json=duplicate_payload)
    
    assert response.status_code == HTTPStatus.CONFLICT
    assert "already exists" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_receptionist_can_get_patient_by_cpf(receptionist_client, seed_patient):
    """
    Verifies that a receptionist can retrieve a patient record using their CPF.
    """
    response = await receptionist_client.get(f"/patients/{seed_patient.cpf}")
    
    assert response.status_code == HTTPStatus.OK
    assert response.json()["name"] == seed_patient.name

@pytest.mark.asyncio
async def test_get_patient_not_found(receptionist_client):
    """
    Validates a 404 response when querying a non-existent patient CPF.
    """
    response = await receptionist_client.get("/patients/999.999.999-99")
    
    assert response.status_code == HTTPStatus.NOT_FOUND

@pytest.mark.asyncio
async def test_receptionist_can_update_patient(receptionist_client, seed_patient):
    """
    Verifies that partial updates to a patient's demographics are successful.
    """
    patient_id = str(seed_patient.id)
    update_payload = {
        "phone_num": "(22) 88888-8888",
        "companion": True
    }
    
    response = await receptionist_client.put(f"/patients/{patient_id}", json=update_payload)
    
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["phone_num"] == "(22) 88888-8888"
    assert data["companion"] is True

    assert data["cpf"] == seed_patient.cpf

@pytest.mark.asyncio
async def test_update_patient_not_found(receptionist_client):
    """
    Tests update failure when the target patient ID is invalid.
    """
    fake_id = str(PydanticObjectId())
    update_payload = {"phone_num": "00000"}
    
    response = await receptionist_client.put(f"/patients/{fake_id}", json=update_payload)
    assert response.status_code == HTTPStatus.NOT_FOUND

@pytest.mark.asyncio
async def test_receptionist_can_check_in_patient(receptionist_client, seed_patient, seed_receptionist):
    """
    Tests the triage initiation process. 
    Verifies a ServiceSheet is created and linked to the patient and receptionist.
    """
    patient_id = str(seed_patient.id)

    response = await receptionist_client.post(f"/patients/{patient_id}/triage")
    
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    
    assert data["patient_ref"] == patient_id

    assert data["receptionist_ref"] == str(seed_receptionist.id)
    assert data["status"] == "aguardando_triagem"

@pytest.mark.asyncio
async def test_check_in_patient_not_found(receptionist_client):
    """
    Validates a 404 response when attempting to check in a non-existent patient.
    """
    fake_id = str(PydanticObjectId())
    response = await receptionist_client.post(f"/patients/{fake_id}/triage")
    
    assert response.status_code == HTTPStatus.NOT_FOUND

@pytest.mark.asyncio
async def test_unauthenticated_access_is_blocked(guest_client):
    """
    Guarantees that requests without a JWT token receive 401 Unauthorized
    on patient endpoints.
    """
    response = await guest_client.get("/patients/111.222.333-44")
    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_update_patient_unauthorized_fields_rejected(receptionist_client, seed_patient):
    """
    Verifies that attempting to update restricted fields (like 'name' or 'cpf')
    returns a 400 Bad Request with a custom detail string for the frontend.
    """
    patient_id = str(seed_patient.id)
    
    invalid_payload = {
        "phone_num": "(22) 99999-9999",
        "name": "Nome Hackeado" 
    }
    
    response = await receptionist_client.put(f"/patients/{patient_id}", json=invalid_payload)
    
    assert response.status_code == HTTPStatus.BAD_REQUEST
    data = response.json()
    
    assert "detail" in data
    assert "Update failed. Unauthorized fields detected: name" in data["detail"]