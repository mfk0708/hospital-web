from fastapi import FastAPI
from routers import dashboard,checkup,pathology,intake,prescription,count,patient

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                    "https://b799-2409-40f4-128-8af0-85c3-7e3d-598-de5b.ngrok-free.app"],  # or ["http://localhost:3000"] to restrict
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



