from fastapi import APIRouter, HTTPException
from database import patients_collection
from schema import PatientCreate
from utils.id_generator import get_next_sequence
from pymongo.errors import PyMongoError

router = APIRouter()

@router.post("/patients")
def create_patient(patient: PatientCreate):
    try:
        patient_id = get_next_sequence("pat")  # Step 1: Generate ID first
        received_data = patient.dict()         # Step 2: Get received data

        # Step 3: Manually create dict with patient_id first
        patient_data = {"patient_id": patient_id, **received_data}

        patients_collection.insert_one(patient_data)  # Step 4: Insert
        return {"message": "Patient added successfully", "patient_id": patient_id}

    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/patients/{patient_id}")
def delete_patient(patient_id: str):
    try:
        result = patients_collection.delete_one({"patient_id": patient_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        return {"message": f"Patient with ID {patient_id} deleted successfully"}
    
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=str(e))