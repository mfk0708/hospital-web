from fastapi import APIRouter,HTTPException
from datetime import date
from database import appointments_collection


router= APIRouter()

@router.get("/count/{patient_id}")
def track_appointment_counts(patient_id: str):
    today = date.today().isoformat()

    pipeline = [
        {"$match": {"patient_id": patient_id}},
        {"$project": {
            "status": 1,
            "is_upcoming": {
                "$cond": [
                    {"$and": [
                        {"$eq": ["$status", "Scheduled"]},
                        {"$gte": ["$date", today]}
                    ]},
                    True,
                    False
                ]
            }
        }},
        {"$group": {
            "_id": None,
            "completed": {"$sum": {"$cond": [{"$eq": ["$status", "Completed"]}, 1, 0]}},
            "cancelled": {"$sum": {"$cond": [{"$eq": ["$status", "Cancelled"]}, 1, 0]}},
            "upcoming": {"$sum": {"$cond": ["$is_upcoming", 1, 0]}}
        }}
    ]

    result = list(appointments_collection.aggregate(pipeline))

    if not result:
        raise HTTPException(status_code=404, detail="No appointments found")

    final_result= result[0]
    final_result.pop("_id", None)

    return final_result

@router.get('/appointments')
def find_appointments():
    appointment=list(appointments_collection.find({},{'_id':0}))
    return appointment