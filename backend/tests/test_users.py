import pytest
from http import HTTPStatus
from beanie import PydanticObjectId

@pytest.mark.asyncio
async def test_admin_can_list_all_users(admin_client, seed_doctor, seed_nurse, seed_receptionist):
    """
    Verifies that an authorized administrator can retrieve the full staff list.
    
    The inclusion of multiple seeds as arguments ensures the database is 
    populated before the GET request is executed.
    """
    response = await admin_client.get("/users/")
    
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert isinstance(data, list)

    assert len(data) >= 4 

@pytest.mark.asyncio
async def test_admin_can_get_user_by_id(admin_client, seed_nurse):
    """
    Ensures a specific user can be retrieved using their unique database ID.
    """
    user_id = str(seed_nurse.id)
    response = await admin_client.get(f"/users/{user_id}")
    
    assert response.status_code == HTTPStatus.OK
    assert response.json()["email"] == seed_nurse.email
    assert response.json()["id"] == user_id

@pytest.mark.asyncio
async def test_get_user_not_found(admin_client):
    """
    Validates the 404 response when searching for a non-existent user ID.
    """
    fake_id = str(PydanticObjectId())
    response = await admin_client.get(f"/users/{fake_id}")
    
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Incorrect user ID or user does not exist in the database."

@pytest.mark.asyncio
async def test_admin_can_create_new_staff(admin_client):
    """
    Ensures the administrator can register new users with valid data.
    """
    new_user_payload = {
        "name": "Dra. Helena Costa",
        "email": "helena@medgemma.com.br",
        "cpf": "999.888.777-66",
        "rg": "RJ-99.888",
        "role": "doctor",
        "specialization": "Neurologia",
        "password": "secure_password_2026"
    }
    
    response = await admin_client.post("/users/", json=new_user_payload)
    
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["email"] == "helena@medgemma.com.br"
    assert "password" not in data

@pytest.mark.asyncio
async def test_create_user_conflict_duplicate_email(admin_client, seed_admin):
    """
    Tests the business rule preventing registration of duplicate emails or CPFs.
    """
    duplicate_payload = {
        "name": "Clone User",
        "email": seed_admin.email,
        "cpf": seed_admin.cpf,
        "rg": "RG-DUP-01",
        "role": "admin",
        "password": "password123"
    }
    
    response = await admin_client.post("/users/", json=duplicate_payload)
    
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()["detail"] == "User with this Email or CPF already exists."

@pytest.mark.asyncio
async def test_admin_can_update_user_role(admin_client, seed_nurse):
    """
    Verifies that the admin can modify an existing user's attributes.
    """
    user_id = str(seed_nurse.id)
    update_payload = {
        "name": "Nurse Updated Name",
        "role": "admin"
    }
    
    response = await admin_client.put(f"/users/{user_id}", json=update_payload)
    
    assert response.status_code == HTTPStatus.OK
    assert response.json()["role"] == "admin"
    assert response.json()["name"] == "Nurse Updated Name"

@pytest.mark.asyncio
async def test_update_user_not_found(admin_client):
    """
    Tests update failure when the target user ID is invalid.
    """
    fake_id = str(PydanticObjectId())
    update_payload = {"name": "No Body"}
    
    response = await admin_client.put(f"/users/{fake_id}", json=update_payload)
    assert response.status_code == HTTPStatus.NOT_FOUND

@pytest.mark.asyncio
async def test_admin_can_delete_user(admin_client, seed_doctor):
    """
    Ensures the administrator can successfully remove a staff member.
    """
    user_id = str(seed_doctor.id)
    
    response = await admin_client.delete(f"/users/{user_id}")
    assert response.status_code == HTTPStatus.NO_CONTENT
    
    get_response = await admin_client.get(f"/users/{user_id}")
    assert get_response.status_code == HTTPStatus.NOT_FOUND

@pytest.mark.asyncio
async def test_delete_user_not_found(admin_client):
    """
    Validates 404 behavior when attempting to delete a non-existent ID.
    """
    fake_id = str(PydanticObjectId())
    response = await admin_client.delete(f"/users/{fake_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND

@pytest.mark.asyncio
async def test_nurse_cannot_list_users(nurse_client):
    """
    Validates RBAC: ensures non-admin roles are forbidden from staff management.
    """
    response = await nurse_client.get("/users/")
    assert response.status_code == HTTPStatus.FORBIDDEN

@pytest.mark.asyncio
async def test_unauthenticated_access_is_blocked(guest_client):
    """
    Guarantees that requests without a JWT token receive 401 Unauthorized.
    """
    response = await guest_client.get("/users/")
    assert response.status_code == HTTPStatus.UNAUTHORIZED