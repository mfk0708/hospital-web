from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from pymongo import DESCENDING
from database import pathology_collection, doctors_collection, db
from datetime import datetime
from utils.id_generator import get_next_sequence
from bson import ObjectId
import gridfs

router = APIRouter()
fs = gridfs.GridFS(db)



router = APIRouter()
fs = gridfs.GridFS(db)
def convert_objectid(doc):
    doc['_id'] = str(doc['_id'])
    return doc

@router.post('/pathology')
async def create_pathology_report(
    pat_id: str = Form(...),
    test_name: str = Form(...),
    result: str = Form(...),
    file: UploadFile = File(None)
):
    report_id = get_next_sequence('rep')
    date_today = datetime.today().strftime("%Y-%m-%d")
    file_id = None
    file_type = None

    if file:
        contents = await file.read()
        file_type = file.content_type
        file_id = fs.put(contents, filename=file.filename, content_type=file_type)

    report_doc = {
        "report_id": report_id,
        "patient_id": pat_id,  # ✅ Use 'patient_id' instead of 'pat_id'
        "test_name": test_name,
        "test_result": result,  # ✅ Optional: Rename 'result' to 'test_result' for consistency
        "date": date_today,
        "status": "Completed",
        "file_id": str(file_id) if file_id else None,
        "file_type": file_type
    }

    pathology_collection.insert_one(report_doc)
    report_doc.pop("_id", None)

    return {
        "message": "Pathology report added successfully.",
        "report": report_doc
    }




# Fetch reports by patient_id
@router.get('/pathology/{patient_id}')
def find_pathology_by_patient(patient_id: str):
    pathology_reports = list(
        pathology_collection.find(
            {"patient_id": patient_id},  # <- changed from "pat_id"
            {"_id": 0}
        ).sort("date", DESCENDING)
    )

    if not pathology_reports:
        raise HTTPException(status_code=404, detail=f"No pathology reports found for patient_id {patient_id}")

    return pathology_reports



# Delete report by report_id
@router.delete('/pathology/{report_id}')
def delete_pathology_report(report_id: str):
    report = pathology_collection.find_one({"report_id": report_id})
    if not report:
        raise HTTPException(status_code=404, detail=f"Pathology report {report_id} not found.")

    # Delete associated file if present
    if "file_id" in report:
        fs.delete(ObjectId(report["file_id"]))

    pathology_collection.delete_one({"report_id": report_id})
    return {"message": f"Pathology report {report_id} deleted successfully."}


# Get all doctors
@router.get("/doctor")
def find_doc():
    docs = list(doctors_collection.find({}, {"_id": 0}))
    return [convert_objectid(doc) for doc in docs]


# Utility to convert ObjectId to string
def convert_objectid(doc):
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
    return doc


# Get image or pdf file from GridFS
@router.get("/file/{file_id}")
def get_file(file_id: str):
    try:
        file = fs.get(ObjectId(file_id))
        content_type = file.content_type or "application/octet-stream"
        return StreamingResponse(file, media_type=content_type)
    except:
        raise HTTPException(status_code=404, detail="File not found")
