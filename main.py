from fastapi import FastAPI
from routers import dashboard, checkup, pathology, intake, prescription, count, patient
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.responses import Response

load_dotenv()
app = FastAPI()

API_KEY = os.getenv("API_KEY")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://healthdash-app.netlify.app","http://localhost:5173","http://localhost:5174"],  # include protocol
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

@app.get("/")
def read_root():
    return {"message": "Hospital API is running"}

@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)  # no content

