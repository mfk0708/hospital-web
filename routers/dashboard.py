from fastapi import APIRouter,HTTPException
from datetime import datetime
from database import appointments_collection,patients_collection,doctors_collection
from utils.id_generator import get_next_sequence
from schema import AppointmentCreate,StatusUpdate
from pymongo import ReturnDocument
from schema import DashboardUpdate



router= APIRouter()

def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d-%m-%Y")
    except:
        return date_str



@router.get("/dashboard")
def get_dashboard_data():
    try:
        pipeline = [
            {
                "$group": {
                    "_id": "$patient_id",
                    "appointment_id": {"$first": "$appointment_id"},
                    "date": {"$first": "$date"},
                    "time": {"$first": "$time"},
                    "doctor_id": {"$first": "$doctor_id"},
                    "status": {"$first": "$status"}
                }
            }
        ]

        appointments = list(appointments_collection.aggregate(pipeline))

        patient_ids = [appt["_id"] for appt in appointments]
        doctor_ids = list(set(appt["doctor_id"] for appt in appointments))

        patients = {
            p["patient_id"]: p
            for p in patients_collection.find({"patient_id": {"$in": patient_ids}}, {"_id": 0})
        }

        doctors = {
            d["doctor_id"]: d["name"]
            for d in doctors_collection.find({"doctor_id": {"$in": doctor_ids}}, {"_id": 0, "doctor_id": 1, "name": 1})
        }

        dashboard = []

        for appt in appointments:
            pid = appt["_id"]
            patient = patients.get(pid)
            doctor_name = doctors.get(appt["doctor_id"], "-")

            if patient:
                disease = "-"
                if patient.get("medical_history"):
                    latest = max(patient["medical_history"], key=lambda h: h["date"])
                    disease = latest.get("description", "-")

                dashboard.append({
                    "appointment_id": appt["appointment_id"],
                    "patient_id": pid,
                    "date": format_date(appt["date"]),  # Expects format_date to return dd-mm-yyyy
                    "time": appt["time"],                # Expected format: HH:MM
                    "status": appt["status"],
                    "patient_name": patient["name"],
                    "patient_age": patient["age"],
                    "gender": patient.get("gender", "-"),
                    "blood_group": patient["blood_group"],
                    "disease": disease,
                    "doctor_name": doctor_name
                })

        # ✅ Sort dashboard by actual datetime (date + time)
      # ✅ Sort by closeness to current datetime (past or future)
        now = datetime.now()
        dashboard.sort(
            key=lambda x: abs(datetime.strptime(f"{x['date']} {x['time']}", "%d-%m-%Y %H:%M") - now)
        )

        return dashboard

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.put("/dashboard/{appointment_id}/{patient_id}")
async def update_dashboard_entry(appointment_id: str, patient_id: str, update_data: DashboardUpdate):
    update_fields = {k: v for k, v in update_data.dict().items() if v is not None}

    if not update_fields:
        raise HTTPException(status_code=400, detail="No update fields provided")

    # Get the appointment to find doctor_id
    appointment = appointments_collection.find_one(
        {"appointment_id": appointment_id, "patient_id": patient_id}
    )
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # Split fields to update different collections
    appointment_updates = {
        k: v for k, v in update_fields.items()
        if k in ['date', 'time', 'status', 'doctor_name']
    }

    patient_updates = {
        "name": update_fields.get("patient_name"),
        "age": update_fields.get("patient_age"),
        "gender": update_fields.get("gender"),
        "blood_group": update_fields.get("blood_group"),
    }
    # Remove keys with None values
    patient_updates = {k: v for k, v in patient_updates.items() if v is not None}

    # Update appointments collection
    if appointment_updates:
        appointments_collection.update_one(
            {"appointment_id": appointment_id, "patient_id": patient_id},
            {"$set": appointment_updates}
        )

    # Update doctors collection if doctor_name is changed
    if "doctor_name" in update_fields:
        doctors_collection.update_one(
            {"doctor_id": appointment['doctor_id']},
            {"$set": {"name": update_fields['doctor_name']}}
        )

    # Update patients collection if patient info is provided
    if patient_updates:
        patients_collection.update_one(
            {"patient_id": patient_id},
            {"$set": patient_updates}
        )

    # Return the updated appointment info
    updated = appointments_collection.find_one(
        {"appointment_id": appointment_id, "patient_id": patient_id},
        {"_id": 0}
    )

    return updated



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
        {"$set": {"status": status.status}},
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



