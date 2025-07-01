from fastapi import APIRouter, HTTPException
from schema import PathologyReport,PathologyReportIn
from pymongo import DESCENDING
from database import pathology_collection
from datetime import datetime
from utils.id_generator import get_next_sequence


router = APIRouter()


@router.post('/pathology')
def create_pathology_report(report: PathologyReportIn):
    report_id = get_next_sequence('rep')
    date_today = datetime.today().strftime("%Y-%m-%d")

    full_report = PathologyReport(
        report_id=report_id,
        date=date_today,
        **report.dict()
    )

    pathology_collection.insert_one(full_report.dict())

    return {
        "message": "Pathology report added successfully.",
        **full_report.dict()
    }

@router.get('/pathology/{patient_id}')
def find_pathology_by_patient(patient_id: str):
    pathology_reports = list(
        pathology_collection.find(
            {"patient_id": patient_id},
            {"_id": 0}
        ).sort("date", DESCENDING)
    )

    if not pathology_reports:
        raise HTTPException(status_code=404, detail=f"No pathology reports found for patient_id {patient_id}")

    return pathology_reports

@router.delete('/pathology/{report_id}')
def delete_pathology_report(report_id: str):
    result = pathology_collection.delete_one({"report_id": report_id})
    if result.deleted_count == 1:
        return {"message": f"Pathology report {report_id} deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail=f"Pathology report {report_id} not found.")
