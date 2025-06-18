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
        # Get the latest appointment per patient
        pipeline = [
            {"$sort": {"date": -1}},  # Sort latest first
            {
                "$group": {
                    "_id": "$patient_id",
                    "date": {"$first": "$date"},
                    "time": {"$first": "$time"}
                }
            }
        ]
        appointments = list(appointments_collection.aggregate(pipeline))

        patient_ids = [appt["_id"] for appt in appointments]

        # Bulk fetch patient details
        patients = {
            p["patient_id"]: p
            for p in patients_collection.find({"patient_id": {"$in": patient_ids}}, {"_id": 0})
        }

        dashboard = []

        for appt in appointments:
            pid = appt["_id"]
            patient = patients.get(pid)

            if patient:
                disease = "-"
                if patient.get("medical_history"):
                    latest = max(patient["medical_history"], key=lambda h: h["date"])
                    disease = latest.get("description", "-")

                dashboard.append({
                    "patient_id": pid,
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


    
@router.get('/patients')
def find_patient():
    patient=list(patients_collection.find({},{'_id':0}))
    return patient