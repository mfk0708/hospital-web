from fastapi import APIRouter,HTTPException
from datetime import datetime
from database import appointments_collection,patients_collection
from utils.id_generator import get_next_sequence
from schema import AppointmentCreate,StatusUpdate
from pymongo import ReturnDocument


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



@router.post("/appointments")
def create_appointment(data: AppointmentCreate):
    conflict = appointments_collection.find_one({
        "doctor_id": data.doctor_id,
        "date": data.date,
        "time": data.time,
        "status": {"$ne": "Cancelled"}
    })

    if conflict:
        return {"error": "Time slot is already booked for this doctor"}

    # Generate unique appointment_id
    appointment_id = get_next_sequence("apt")

    new_appointment = {
        "appointment_id": appointment_id,
        **data.dict()
    }

    appointments_collection.insert_one(new_appointment)

    return {
    "message": "Appointment created successfully",
    "appointment_id": new_appointment["appointment_id"]
}


@router.patch('/appointments/{apt_id}')
def update_appstatus(apt_id: str, status: StatusUpdate):
    updated_appointment = appointments_collection.find_one_and_update(
        {"appointment_id": apt_id},
        {"$set": {"status": status.status}},  # <- Fix here: extract enum value
        return_document=ReturnDocument.AFTER
    )

    if not updated_appointment:
        return {"message": "Appointment cannot be found"}

    # Remove the _id key before returning
    updated_appointment.pop("_id", None)

    return {
        "message": "Appointment status updated successfully",
        "appointment": updated_appointment
    }

    
@router.get('/appointments')
def find_appointments():
    appointment = list(appointments_collection.find({},{"_id":0}))
    return appointment


@router.delete("/appointments/{appointment_id}")
def delete_appointments(appointment_id: str):
    result = appointments_collection.delete_one({"appointment_id": appointment_id})

    if result.deleted_count == 1:
        return {"message": f"Appointment {appointment_id} deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail=f"Appointment {appointment_id} not found.")



