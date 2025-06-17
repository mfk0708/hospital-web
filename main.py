from fastapi import FastAPI
from routers import dashboard,checkup,pathology,intake,prescription,count


app = FastAPI()

app.include_router(dashboard.router)
app.include_router(checkup.router)
app.include_router(count.router)
app.include_router(prescription.router)
app.include_router(pathology.router)
app.include_router(intake.router)



