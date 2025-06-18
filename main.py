from fastapi import FastAPI
from routers import dashboard,checkup,pathology,intake,prescription,count

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["http://localhost:3000"] to restrict
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



