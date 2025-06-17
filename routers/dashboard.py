from fastapi import APIRouter,HTTPException
from datetime import datetime
from database import appointments_collection,patients_collection,doctors_collection


router= APIRouter()

def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d-%m-%Y")
    except:
        return date_str





@router.get("/dashboard")
def get_dashboard_data():
    try:
        dashboard = []

        appointments = list(appointments_collection.find({}, {
            "_id": 0,
            "patient_id": 1,
            "date": 1,
            "time": 1
        }))

        for appt in appointments:
            patient = patients_collection.find_one(
                {"patient_id": appt["patient_id"]},
                {"_id": 0,}
            )

            if patient:
                # Get latest disease from medical history
                disease = "-"
                if patient.get("medical_history"):
                    latest = max(patient["medical_history"], key=lambda h: h["date"])
                    disease = latest.get("description", "-")

                dashboard.append({
                    "patient_id":patient["patient_id"],
                    "date": format_date(appt["date"]),
                    "time": appt["time"],
                    "patient_name": patient["name"],
                    "patient_age": patient["age"],
                    "blood_group": patient["blood_group"],
                    "disease": disease
                })

        return dashboard

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/doctors")
def find_doctor():
    doctor=list(doctors_collection.find({},{"_id":0}))
    return doctor