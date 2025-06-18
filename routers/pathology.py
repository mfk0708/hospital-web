from fastapi import APIRouter
from pymongo import DESCENDING
from database import pathology_collection

router = APIRouter()

@router.get('/pathology/{patient_id}')
def find_pathology(patient_id: str):
    pathology = list(
        pathology_collection.find(
            {'patient_id': patient_id}, {'_id': 0}
        ).sort('date', DESCENDING)
    )
    return pathology
