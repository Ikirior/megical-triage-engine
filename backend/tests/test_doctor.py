import pytest
from http import HTTPStatus
from beanie import PydanticObjectId
from contracts import TriageStatus

@pytest.mark.asyncio
async def test_doctor_can_get_prioritized_queue(doctor_client, seed_ready_service_sheet, seed_patient):
    """
    Verifies that a doctor can retrieve the list of patients ready for consultation.
    """
    response = await doctor_client.get("/doctors/queue")
    
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["patient_name"] == seed_patient.name
    assert data[0]["risk_classification"] == "verde"

@pytest.mark.asyncio
async def test_doctor_can_start_consultation(doctor_client, seed_ready_service_sheet):
    """
    Verifies that a doctor can transition a sheet from 'waiting' to 'in progress'.
    """
    sheet_id = str(seed_ready_service_sheet.id)
    response = await doctor_client.post(f"/doctors/{sheet_id}/start")
    
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["status"] == TriageStatus.em_atendimento

    assert "patient" in data
    assert data["patient"]["cpf"] == "000.111.222-33"

@pytest.mark.asyncio
async def test_start_consultation_conflict_error(doctor_client, seed_ready_service_sheet):
    """
    Ensures a 400 error is raised if the patient is already being attended.
    """
    sheet_id = str(seed_ready_service_sheet.id)
    
    await doctor_client.post(f"/doctors/{sheet_id}/start")
    
    response = await doctor_client.post(f"/doctors/{sheet_id}/start")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "not available" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_doctor_can_finish_consultation(doctor_client, seed_ready_service_sheet):
    """
    Tests the full completion of a medical service and status update to 'finalizado'.
    """
    sheet_id = str(seed_ready_service_sheet.id)
    
    await doctor_client.post(f"/doctors/{sheet_id}/start")
    
    finish_payload = {
        "doctor_notes": "Paciente apresentando melhora clínica.",
        "diagnosis_cid": "Z00.0",
        "prescription": "Repouso e hidratação.",
        "ai_pre_consultation_summary": "Resumo gerado anteriormente pela IA."
    }
    
    response = await doctor_client.post(f"/doctors/{sheet_id}/finish", json=finish_payload)
    
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["status"] == TriageStatus.finalizado
    assert data["doctor_data"]["diagnosis_cid"] == "Z00.0"

@pytest.mark.asyncio
async def test_unauthorized_doctor_cannot_finish_other_service(doctor_client, admin_client, seed_ready_service_sheet):
    """
    RBAC and Ownership Test: Ensures only the doctor assigned to the sheet can finish it.
    
    We use admin_client here to simulate a different authenticated user trying to 
    intercept a consultation assigned to the seed_doctor.
    """
    sheet_id = str(seed_ready_service_sheet.id)
    
    await doctor_client.post(f"/doctors/{sheet_id}/start")
    
    response = await admin_client.post(f"/doctors/{sheet_id}/finish", json={"doctor_notes": "hack"})
    
    assert response.status_code == HTTPStatus.FORBIDDEN

@pytest.mark.asyncio
async def test_get_doctor_queue_unauthenticated(guest_client):
    """
    Guarantees that requests without a JWT token receive 401 Unauthorized.
    """
    response = await guest_client.get("/doctors/queue")
    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_doctor_can_get_own_session(doctor_client, seed_ready_service_sheet):
    """
    Verifies that a doctor can recover their active consultation session.
    """
    sheet_id = str(seed_ready_service_sheet.id)

    start_response = await doctor_client.post(f"/doctors/{sheet_id}/start")
    assert start_response.status_code == HTTPStatus.OK
    
    response = await doctor_client.get(f"/doctors/{sheet_id}/session")

    if response.status_code == HTTPStatus.UNAUTHORIZED:
        print(f"Debug Detail: {response.json()}")

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["id"] == sheet_id
    assert data["doctor_ref"] is not None

@pytest.mark.asyncio
async def test_doctor_cannot_get_other_doctor_session(doctor_client, admin_client, seed_ready_service_sheet):
    """
    Ensures a doctor cannot read the session of a patient assigned to another doctor.
    We use admin_client here to simulate a different authenticated user binding the sheet.
    """
    sheet_id = str(seed_ready_service_sheet.id)
    
    await admin_client.post(f"/doctors/{sheet_id}/start")
    
    response = await doctor_client.get(f"/doctors/{sheet_id}/session")
    
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert "does not have access" in response.json()["detail"].lower()