from fastapi import APIRouter,HTTPException
from schema import PrescriptionIn,Prescription
from pymongo import DESCENDING
from database import prescription_collection
from datetime import datetime
from utils.id_generator import get_next_sequence


router =APIRouter()


@router.post('/prescription')
def create_prescription(prescription: PrescriptionIn):
    # Add ID and date here
    full_prescription = Prescription(
        **prescription.dict(),
        prescription_id=get_next_sequence("presc"),
        date=datetime.today().strftime("%Y-%m-%d")
    )

    prescription_collection.insert_one(full_prescription.dict())

    return {
        "message": "Prescription added successfully.",
        **full_prescription.dict()
    }

    
@router.get('/prescription/{patient_id}')
def get_prescriptions_by_patient(patient_id: str):
    prescriptions = list(
        prescription_collection.find(
            {"patient_id": patient_id},
            {"_id": 0}
        ).sort("date", DESCENDING)
    )
    if not prescriptions:
        raise HTTPException(status_code=404, detail=f"No prescriptions found for patient_id {patient_id}")

    return {
        "message": f"Found {len(prescriptions)} prescription(s) for patient_id {patient_id}.",
        "prescriptions": prescriptions
    }
    
@router.delete('/prescription/{prescription_id}')
def delete_prescription(prescription_id: str):
    result = prescription_collection.delete_one({"prescription_id": prescription_id})
    if result.deleted_count == 1:
        return {"message": f"Prescription {prescription_id} deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail=f"Prescription {prescription_id} not found.")