from pydantic import BaseModel,Field
from typing import Optional, List
from enum import Enum
from bson import ObjectId

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
    doctor_comments: Optional[List[str]] = Field(default_factory=list)  

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
    doctor_comments: Optional[List[str]] = None



class AppointmentCreate(BaseModel):
    patient_id: str
    doctor_id: str
    date: str 
    time: str
    status: str = "Scheduled"


class AppointmentStatus(str, Enum):
    completed = "Completed"
    scheduled = "Scheduled"
   

    
class StatusUpdate(BaseModel):
    status: AppointmentStatus

class PrescriptionIn(BaseModel):
    patient_id: str
    medicine: str
    dosage: str
    frequency: str
    duration: str
    notes: str

class Prescription(PrescriptionIn):
    prescription_id: str
    date: str

class PathologyReportIn(BaseModel):
    pat_id: str
    test_name: str
    result: str

class PathologyReport(BaseModel):
    report_id: str
    pat_id: str
    test_name: str
    result: str
    date: str
    status: str
    file_path: Optional[str] = None  


class DashboardUpdate(BaseModel):
    date: Optional[str]
    time: Optional[str]
    status: Optional[str]
    patient_name: Optional[str]
    patient_age: Optional[int]
    gender: Optional[str]
    blood_group: Optional[str]
    disease: Optional[str]
    doctor_name: Optional[str]


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

class PathologyResponseModel(BaseModel):
    id: PyObjectId = Field(..., alias="_id")
    name: str
    # add other fields...

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }    