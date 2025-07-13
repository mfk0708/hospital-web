from fastapi import FastAPI
from routers import dashboard,checkup,pathology,intake,prescription,count,patient
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os


load_dotenv()
app = FastAPI()


API_KEY = os.getenv("API_KEY")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(dashboard.router)
app.include_router(checkup.router)
app.include_router(count.router)
app.include_router(prescription.router)
app.include_router(pathology.router)
app.include_router(intake.router)
app.include_router(patient.router)



