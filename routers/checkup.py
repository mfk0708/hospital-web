from fastapi import APIRouter,HTTPException
from database import patients_collection,appointments_collection,doctors_collection


router= APIRouter()

@router.get("/checkup/{patient_id}")
def get_doctor_checkup_history(patient_id: str):
    try:
        # Fetch patient
        patient = patients_collection.find_one(
            {"patient_id": patient_id},
            {"_id": 0, "medical_history": 1}
        )

        if not patient or "medical_history" not in patient or not patient["medical_history"]:
            raise HTTPException(status_code=404, detail="Patient not found or no medical history")

        # Fetch all appointments of the patient
        appointments = list(appointments_collection.find(
            {"patient_id": patient_id},
            {"_id": 0, "doctor_id": 1, "date": 1}
        ))

        # Sort appointments by date (ascending)
        appointments.sort(key=lambda x: x["date"])

        checkups = []

        for history in patient["medical_history"]:
            disease_date = history["date"]
            disease_desc = history["description"]

            # Get all appointments on or after the disease date
            matched_appointments = [
                appt for appt in appointments if appt["date"] >= disease_date
            ]

            if matched_appointments:
                for appt in matched_appointments:
                    doctor = doctors_collection.find_one(
                        {"doctor_id": appt["doctor_id"]},
                        {"_id": 0, "name": 1, "specialization": 1}
                    )

                    checkups.append({
                        "name": doctor["name"] if doctor else "Unknown",
                        "specialization": doctor["specialization"] if doctor else "Unknown",
                        "disease": disease_desc,
                        "date": appt["date"]  # Use appointment date for sorting
                    })
            else:
                checkups.append({
                    "name": "No doctor found",
                    "specialization": "N/A",
                    "disease": disease_desc,
                    "date": disease_date
                })

        checkups.sort(key=lambda x: x["date"], reverse=True)

        return checkups

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
