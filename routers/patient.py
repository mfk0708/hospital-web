from fastapi import APIRouter, HTTPException
from database import patients_collection
from schema import PatientCreate, UpdatePatientModel
from utils.id_generator import get_next_sequence
from pymongo.errors import PyMongoError
from bson import ObjectId

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
    
from pymongo import UpdateOne

@router.put("/patients/{patient_id}")
def update_patient(patient_id: str, updated_data: UpdatePatientModel):
    update_dict = updated_data.dict(exclude_none=True)

    if not update_dict:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    patient = patients_collection.find_one({"patient_id": patient_id})
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found")

    update_query = {}

    # ✅ Handle intake_form.vital_signs merging
    if "intake_form" in update_dict:
        if "vital_signs" in update_dict["intake_form"]:
            existing_vs = patient.get("intake_form", {}).get("vital_signs", {})
            new_vs = update_dict["intake_form"]["vital_signs"]
            update_dict["intake_form"]["vital_signs"] = {**existing_vs, **new_vs}

        # Merge full intake_form
        existing_intake = patient.get("intake_form", {})
        new_intake = update_dict["intake_form"]
        update_dict["intake_form"] = {**existing_intake, **new_intake}

    # ✅ Handle appending to medical_history
    if "medical_history" in update_dict:
        update_query["$push"] = {
            "medical_history": {
                "$each": update_dict.pop("medical_history")
            }
        }

    # ✅ Handle remaining fields with $set
    if update_dict:
        update_query["$set"] = update_dict

    # Perform update
    patients_collection.update_one({"patient_id": patient_id}, update_query)

    return {
        "message": "Patient updated successfully",
        "updated_fields": update_query
    }
