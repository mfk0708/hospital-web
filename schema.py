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

class PartialVitalSigns(BaseModel):
    blood_pressure: Optional[str] = None
    temperature: Optional[str] = None
    pulse: Optional[int] = None

class PartialIntakeForm(BaseModel):
    date: Optional[str] = None
    vital_signs: Optional[PartialVitalSigns] = None

class UpdatePatientModel(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    profile_picture: Optional[str] = None
    medical_history: Optional[List[MedicalHistoryItem]] = None
    intake_form: Optional[PartialIntakeForm] = None