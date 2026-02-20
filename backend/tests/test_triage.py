import pytest
from http import HTTPStatus
from beanie import PydanticObjectId

@pytest.mark.asyncio
async def test_nurse_can_get_triage_queue(nurse_client, seed_service_sheet, seed_patient):
    """
    Verifies that a nurse can retrieve the list of patients waiting for triage.
    """
    response = await nurse_client.get("/triages/queue")
    
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    
    queue_item = data[0]
    assert queue_item["sheet_id"] == str(seed_service_sheet.id)
    assert queue_item["patient_id"] == str(seed_patient.id)
    assert queue_item["patient_name"] == seed_patient.name

@pytest.mark.asyncio
async def test_nurse_can_start_triage(nurse_client, seed_service_sheet, seed_nurse):
    """
    Verifies that a nurse can lock a service sheet and start the triage process.
    """
    sheet_id = str(seed_service_sheet.id)
    
    response = await nurse_client.post(f"/triages/{sheet_id}/start")
    
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["status"] == "em_triagem"


@pytest.mark.asyncio
async def test_start_triage_invalid_state_conflict(nurse_client, seed_service_sheet):
    """
    Ensures that a service sheet cannot be started twice, preventing race conditions.
    """
    sheet_id = str(seed_service_sheet.id)
    
    await nurse_client.post(f"/triages/{sheet_id}/start")
    
    response = await nurse_client.post(f"/triages/{sheet_id}/start")
    
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "currently in triage" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_nurse_can_execute_triage_phases_e2e(nurse_client, seed_service_sheet):
    """
    End-to-End integration test for the 3-phase triage workflow.
    
    Simulates the frontend passing data from Phase 1 to Phase 2, and finalizing in Phase 3.
    """
    sheet_id = str(seed_service_sheet.id)
    
    await nurse_client.post(f"/triages/{sheet_id}/start")
    
    phase_one_payload = {
        "vitals": {
            "systolic_bp": 120,
            "diastolic_bp": 80,
            "heart_rate": 85,
            "temperature": 38.5,
            "oxygen_saturation": 98.0
        },
        "nurse_initial_observations": "Paciente relata febre e dores no corpo."
    }
    
    resp_phase_1 = await nurse_client.post(f"/triages/{sheet_id}/phase-one", json=phase_one_payload)
    assert resp_phase_1.status_code == HTTPStatus.OK
    
    questions = resp_phase_1.json()
    assert isinstance(questions, list)
    assert len(questions) > 0
    assert "question_id" in questions[0]
    
    for q in questions:
        q["patient_answer"] = "Sim, começou ontem à noite."
        
    phase_two_payload = {
        "investigation_qa": questions
    }
    
    resp_phase_2 = await nurse_client.post(f"/triages/{sheet_id}/phase-two", json=phase_two_payload)
    assert resp_phase_2.status_code == HTTPStatus.OK
    
    suggestion = resp_phase_2.json()
    assert isinstance(suggestion, str)
    assert "mock" in suggestion.lower()
    
    phase_three_payload = {
        "risk_classification": "amarelo",
        "final_nurse_notes": "Paciente estável, mas com febre persistente."
    }
    
    resp_phase_3 = await nurse_client.post(f"/triages/{sheet_id}/phase-three", json=phase_three_payload)
    assert resp_phase_3.status_code == HTTPStatus.OK
    assert resp_phase_3.json() is True

@pytest.mark.asyncio
async def test_execute_phase_two_without_phase_one_fails(nurse_client, seed_service_sheet):
    """
    Verifies the IncompleteTriageDataError.
    Phase 2 should block execution if Phase 1 (vitals) was never submitted.
    """
    sheet_id = str(seed_service_sheet.id)
    await nurse_client.post(f"/triages/{sheet_id}/start")
    
    phase_two_payload = {"investigation_qa": []}
    
    response = await nurse_client.post(f"/triages/{sheet_id}/phase-two", json=phase_two_payload)
    
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "missing" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_unauthenticated_access_is_blocked(guest_client, seed_service_sheet):
    """
    Guarantees that requests without a JWT token receive 401 Unauthorized
    on triage endpoints.
    """
    response = await guest_client.get("/triages/queue")
    assert response.status_code == HTTPStatus.UNAUTHORIZED