from pydantic import BaseModel,Field
from typing import Optional, List
from enum import Enum

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
    medical_history: Optional[List[MedicalHistoryItem]] = Field(default_factory=list)
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



class AppointmentCreate(BaseModel):
    patient_id: str
    doctor_id: str
    date: str 
    time: str
    status: str = "Scheduled"


class AppointmentStatus(str, Enum):
    cancelled = "Cancelled"
    completed = "Completed"
    scheduled = "Scheduled"
    postponed = "Postponed"

class PrescriptionIn(BaseModel):
    patient_id: str
    doctor_id: str
    medicine: str
    dosage: str
    frequency: str
    duration: str
    notes: str

class Prescription(PrescriptionIn):
    prescription_id: str
    date: str

class PathologyReportIn(BaseModel):
    patient_id: str
    test_name: str
    status: str
    diagnosis: str

class PathologyReport(BaseModel):
    report_id: str
    patient_id: str
    date: str
    test_name: str
    status: str
    diagnosis: str