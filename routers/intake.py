from fastapi import APIRouter,HTTPException
from database import patients_collection


router=APIRouter()

@router.get("/profile/{patient_id}")
def find_patient(patient_id: str):
    # Fetch all documents with the given patient_id
    patients = list(patients_collection.find(
        {"patient_id": patient_id},
        {"_id": 0}
    ))

    if not patients:
        raise HTTPException(status_code=404, detail="No patient found with this ID")

    return patients