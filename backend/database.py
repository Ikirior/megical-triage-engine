import os
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models import User, Patient, ServiceSheet
from services.auth import AuthService

async def _seed_default_admin():
    """
    Verifies the existence of a master administrator and creates one if the database is empty.
    
    This acts as an initial database seeder to ensure the system is never locked out
    upon first deployment.
    """
    
    admin_email = os.getenv("DEFAULT_ADMIN_EMAIL")
    admin_cpf = os.getenv("DEFAULT_ADMIN_CPF")
    
    existing_admin = await User.find_one(User.email == admin_email)
    
    if not existing_admin:
        
        default_password = os.getenv("DEFAULT_ADMIN_PASSWORD")
        password_hash = AuthService.get_password_hash(default_password)
        
        admin_user = User(
            name="Master Administrator",
            email=admin_email,
            cpf=admin_cpf,
            rg="MASTER-01",
            role="admin",
            password_hash=password_hash
        )
        
        await admin_user.insert()
        
        print(f"System Seed: Default admin created with email '{admin_email}'.")

async def init_db():
    """
    Initializes the MongoDB connection and configures the Beanie ODM.
    
    Raises:
        ValueError: If the MONGO_URL environment variable is missing.
    """
    
    mongo_url = os.getenv("MONGO_URL")
    
    if not mongo_url:
        raise ValueError("error: The environment variable 'MONGO_URL' was not set. The system cannot start without a database.")
    
    client = AsyncIOMotorClient(mongo_url)
    
    await init_beanie(
        database = client.megical,
        document_models = [User, Patient, ServiceSheet]
    )
    
    await _seed_default_admin()