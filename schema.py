from pydantic import BaseModel
from typing import Optional, List

class VitalSigns(BaseModel):
    blood_pressure: str
    temperature: str
    pulse: int

class IntakeForm(BaseModel):
    date: str
    vital_signs: VitalSigns

class MedicalHistoryItem(BaseModel):
    date: str
    description: str

class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str
    blood_group: str
    profile_picture: Optional[str] = None
    medical_history: Optional[List[MedicalHistoryItem]] = []
    intake_form: Optional[IntakeForm] = None
