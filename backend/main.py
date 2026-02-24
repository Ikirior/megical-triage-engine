from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers import users, patients, triages, doctors, auth
from database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan, title="MedGemma API")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(patients.router)
app.include_router(triages.router)
app.include_router(doctors.router)

app.get("/")
def root():
    return {"message": "Hello World!"}