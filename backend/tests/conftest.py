import pytest
import pytest_asyncio
from datetime import date
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from main import app
from models import User, Patient, ServiceSheet
from services.auth import AuthService
from contracts import TriageStatus

@pytest_asyncio.fixture(autouse=True, scope="function")
async def setup_test_database():
    """Initializes a fresh isolated test database for every single test function."""
    mongo_url = "mongodb://admin:senha123@localhost:27017/megical_test?authSource=admin"
    client = AsyncIOMotorClient(mongo_url)
    database = client.medgemma_test_db
    
    await client.drop_database("medgemma_test_db")
    
    await init_beanie(database=database, document_models=[User, Patient, ServiceSheet])
    
    yield
    
    client.close()

async def create_test_user(email: str, cpf: str, role: str, name: str) -> User:
    """Utility to create users within the current active loop."""
    password_hash = AuthService.get_password_hash("test_password")
    user = User(
        name=name, email=email, cpf=cpf, rg=f"RG-{cpf[:2]}",
        role=role, password_hash=password_hash
    )
    await user.insert()
    return user

@pytest_asyncio.fixture(scope="function")
async def seed_admin():
    return await create_test_user("admin@test.com", "000.000.000-01", "admin", "Admin Test")

@pytest_asyncio.fixture(scope="function")
async def seed_nurse():
    return await create_test_user("nurse@test.com", "000.000.000-03", "nurse", "Nurse Test")

@pytest_asyncio.fixture(scope="function")
async def seed_doctor():
    return await create_test_user("doctor@test.com", "000.000.000-02", "doctor", "Doctor Test")

@pytest_asyncio.fixture(scope="function")
async def seed_receptionist():
    return await create_test_user("reception@test.com", "000.000.000-04", "receptionist", "Receptionist Test")

async def get_authenticated_client(user: User) -> AsyncClient:
    """Generates an AsyncClient with the correct loop context."""
    token = AuthService.create_access_token({"sub": str(user.id), "role": user.role})
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test", headers={"Authorization": f"Bearer {token}"})

@pytest_asyncio.fixture(scope="function")
async def admin_client(seed_admin):
    async with await get_authenticated_client(seed_admin) as client:
        yield client

@pytest_asyncio.fixture(scope="function")
async def nurse_client(seed_nurse):
    async with await get_authenticated_client(seed_nurse) as client:
        yield client

@pytest_asyncio.fixture(scope="function")
async def guest_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

@pytest_asyncio.fixture(scope="function")
async def receptionist_client(seed_receptionist):
    """Provides an asynchronous client pre-authorized with a Receptionist token."""
    async with await get_authenticated_client(seed_receptionist) as client:
        yield client

@pytest_asyncio.fixture(scope="function")
async def seed_patient():
    """
    Utility to create a base patient within the current active loop.
    
    Ensures that the data strictly follows the Pydantic contracts and Beanie models.
    """
    patient = Patient(
        name="Paciente Teste",
        cpf="000.111.222-33",
        rg="MG-12.345.678",
        birth_date=date(1990, 1, 1),
        address="Rua Seed, 123",
        companion=False,
        race="branca",
        sex="M",
        phone_num="(11) 99999-9999"
    )
    await patient.insert()
    return patient

@pytest_asyncio.fixture(scope="function")
async def seed_service_sheet(seed_patient, seed_receptionist):
    """
    Utility to create a base service sheet waiting in the triage queue.
    """
    sheet = ServiceSheet(
        patient_ref=seed_patient.id,
        receptionist_ref=seed_receptionist.id,
        status=TriageStatus.aguardando_triagem
    )
    await sheet.insert()
    return sheet

@pytest_asyncio.fixture(scope="function")
async def doctor_client(seed_doctor):
    """Provides an asynchronous client pre-authorized with a Doctor token."""
    async with await get_authenticated_client(seed_doctor) as client:
        yield client

@pytest_asyncio.fixture(scope="function")
async def seed_ready_service_sheet(seed_patient, seed_receptionist):
    """
    Utility to create a service sheet that has already cleared triage.
    Status is set to 'aguardando_medico' to test the doctor's flow.
    """
    sheet = ServiceSheet(
        patient_ref=seed_patient.id,
        receptionist_ref=seed_receptionist.id,
        status=TriageStatus.aguardando_medico,
        triage_data={
            "vitals": {
                "systolic_bp": 120, "diastolic_bp": 80, "heart_rate": 70,
                "temperature": 36.5, "oxygen_saturation": 99
            },
            "nurse_initial_observations": "Sinais estáveis.",
            "risk_classification": "verde"
        }
    )
    await sheet.insert()
    return sheet