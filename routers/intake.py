from fastapi import APIRouter,HTTPException
from database import patients_collection


router=APIRouter()

@router.get("/intake/{patient_id}")
def find_intake(patient_id: str):
    patient = patients_collection.find_one(
        {"patient_id": patient_id},
        {"_id": 0, "intake_form": 1}
    )
    if not patient or "intake_form" not in patient:
        raise HTTPException(status_code=404, detail="Intake form not found for this patient")
    
    return patient["intake_form"]