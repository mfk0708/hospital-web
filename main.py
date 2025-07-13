from fastapi import FastAPI, Request
from routers import dashboard, checkup, pathology, intake, prescription, count, patient
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
import os

load_dotenv()
app = FastAPI()

API_KEY = os.getenv("API_KEY")

# ✅ Middleware to enforce API key globally
@app.middleware("http")
async def enforce_api_key(request: Request, call_next):
    if request.url.path == "/favicon.ico":
        return Response(status_code=204)

    api_key = request.headers.get("x-api-key")
    if api_key != API_KEY:
        return JSONResponse(
            status_code=401,
            content={"detail": "Unauthorized: Invalid or missing API Key"}
        )
    
    response = await call_next(request)
    return response

# ✅ CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://healthdash-app.netlify.app", "http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Routers
app.include_router(dashboard.router)
app.include_router(checkup.router)
app.include_router(count.router)
app.include_router(prescription.router)
app.include_router(pathology.router)
app.include_router(intake.router)
app.include_router(patient.router)

# ✅ Routes
@app.get("/")
def read_root():
    return {"message": "Hospital API is running"}
