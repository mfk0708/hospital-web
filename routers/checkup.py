from fastapi import APIRouter, HTTPException
from database import patients_collection, appointments_collection, doctors_collection

router = APIRouter()

@router.get("/checkup/{patient_id}")
def get_doctor_checkup_history(patient_id: str):
    try:
        # 1. Fetch the patient's medical history only
        patient = patients_collection.find_one(
            {"patient_id": patient_id},
            {"_id": 0, "medical_history": 1}
        )

        if not patient or "medical_history" not in patient or not patient["medical_history"]:
            raise HTTPException(status_code=404, detail="Patient not found or no medical history")

        # 2. Fetch all appointments of the patient with required fields
        appointments = list(appointments_collection.find(
            {"patient_id": patient_id},
            {"_id": 0, "doctor_id": 1, "date": 1}
        ))

        if not appointments:
            raise HTTPException(status_code=404, detail="No appointments found")

        # 3. Build map of appointments sorted by date
        appointments.sort(key=lambda x: x["date"])
        
        # 4. Extract unique doctor_ids for batch fetch
        unique_doctor_ids = list({appt["doctor_id"] for appt in appointments})
        
        doctors_cursor = doctors_collection.find(
            {"doctor_id": {"$in": unique_doctor_ids}},
            {"_id": 0, "doctor_id": 1, "name": 1, "specialization": 1}
        )
        doctor_map = {doc["doctor_id"]: doc for doc in doctors_cursor}

        # 5. Prepare the checkup history
        checkups = []
        for history in patient["medical_history"]:
            disease_date = history["date"]
            disease_desc = history["description"]

            matched_appointments = [
                appt for appt in appointments if appt["date"] >= disease_date
            ]

            if matched_appointments:
                for appt in matched_appointments:
                    doctor_info = doctor_map.get(appt["doctor_id"], {"name": "Unknown", "specialization": "Unknown"})

                    checkups.append({
                        "name": doctor_info["name"],
                        "specialization": doctor_info["specialization"],
                        "disease": disease_desc,
                        "date": appt["date"]
                    })
            else:
                checkups.append({
                    "name": "No doctor found",
                    "specialization": "N/A",
                    "disease": disease_desc,
                    "date": disease_date
                })

        # 6. Sort checkups by most recent first
        checkups.sort(key=lambda x: x["date"], reverse=True)

        return checkups

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
