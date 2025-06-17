from fastapi import APIRouter
from database import intake_collections


router=APIRouter()

@router.get('/intake/{patient_id}')
def find_intake(patient_id:str):
    intake= list(intake_collections.find({"patient_id":patient_id},{"_id":0}))
    return intake