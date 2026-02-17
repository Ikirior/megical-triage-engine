import os
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models import User, Patient, ServiceSheet

async def init_db():
    
    mongo_url = os.getenv("MONGO_URL", "mongodb://admin:senha123@localhost:27017?authSource=admin")
    
    client = AsyncIOMotorClient(mongo_url)
    
    await init_beanie(
        database = client.medgemma_db,
        document_models = [User, Patient, ServiceSheet]
    )