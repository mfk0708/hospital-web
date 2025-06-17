from fastapi import APIRouter
from database import prescription_collection

router =APIRouter()

@router.get('/prescription/{patient_id}')
def find_prescription(patient_id: str):
    prescription = list(prescription_collection.find({'patient_id': patient_id}, {'_id': 0}))

    return prescription

