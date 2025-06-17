from fastapi import APIRouter,HTTPException
from datetime import date,datetime
from database import appointments_collection


router= APIRouter()

@router.get("/count/{patient_id}")
def track_appointment_counts(patient_id: str):
    try:
        today = date.today().isoformat()

        # Only get fields we need and exclude _id
        appointments = list(appointments_collection.find(
            {"patient_id": patient_id},
            {"_id": 0, "date": 1, "status": 1}
        ))

        if not appointments:
            raise HTTPException(status_code=404, detail="No appointments found for this patient")

        completed_count = 0
        upcoming_count = 0
        cancelled_count=0

        for app in appointments:
            app_date_raw = app.get("date")

            if not app_date_raw or "status" not in app:
                continue

            # Convert date to ISO string
            if isinstance(app_date_raw, datetime):
                app_date = app_date_raw.date().isoformat()
            else:
                app_date = str(app_date_raw)

            if app["status"] == "Completed":
                completed_count += 1
            
            elif app["status"]=="Cancelled":
                cancelled_count += 1
            elif app["status"] == "Scheduled" and app_date >= today:
                upcoming_count += 1

        return {
            "completed": completed_count,
            "upcoming": upcoming_count,
            "cancelled":cancelled_count
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")