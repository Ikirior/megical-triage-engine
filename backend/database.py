from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models import User, Patient, ServiceSheet

async def init_db():
    
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    
    await init_beanie(
        database = client.medgemma_db,
        document_models = [User, Patient, ServiceSheet]
    )