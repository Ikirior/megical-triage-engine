import os
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models import User, Patient, ServiceSheet

async def init_db():
    
    mongo_url = os.getenv("MONGO_URL")
    
    if not mongo_url:
        raise ValueError("error: The environment variable 'MONGO_URL' was not set. The system cannot start without a database.")
    
    client = AsyncIOMotorClient(mongo_url)
    
    await init_beanie(
        database = client.megical,
        document_models = [User, Patient, ServiceSheet]
    )