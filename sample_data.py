from database import (
    patients_collection,
    appointments_collection,
    doctors_collection,
    prescription_collection,
    intake_collections,
    pathology_collection
)

from datetime import datetime, timedelta
import random
from pymongo.errors import PyMongoError


names = ["Fahad", "Mubarak", "Rifai", "Sheik", "Afrin", "Durga", "Rifqa", "Sathyasri", "Kaleel", "Nivetha"]
blood_groups = ["A +ve", "B +ve", "AB -ve", "O +ve", "A -ve"]
diseases = ["Fever", "Diabetes", "Hypertension", "Asthma", "Allergy"]
medicines = ["Paracetamol", "Metformin", "Cetirizine", "Amoxicillin", "Atorvastatin"]
tests = ["Blood Test", "X-Ray", "MRI", "ECG"]
statuses = ["Pending", "Completed", "In Progress"]
diagnoses = ["Normal", "Infection", "Deficiency", "Chronic Disease"]
specializations = ["General", "Cardiology", "ENT", "Dermatology", "Neurology"]
doctor_name=['Vijay','Dhanush','Ajith','Rajini','Kamal']
try:
    patients_collection.delete_many({})
    doctors_collection.delete_many({})
    appointments_collection.delete_many({})
    prescription_collection.delete_many({})
    intake_collections.delete_many({})
    pathology_collection.delete_many({})

 
    doctors = []
    for i in range(5):
        doctor = {
            "doctor_id": f"doc{i+1}",
            "name": f"Dr. {doctor_name[i]}",
            "specialization": specializations[i],
            "phone": f"+91-98765{1000+i}"
        }
        doctors.append(doctor)
    doctors_collection.insert_many(doctors)

 
    patients = []
    appointments = []
    prescriptions = []
    pathology_reports = []
    intake_forms = []

    for i in range(10):
        patient_id = f"pat{i+1}"
        patient_name = names[i]

        # Patient basic data
        patient = {
            "patient_id": patient_id,
            "name": patient_name,
            "age": 22 if patient_name == "Fahad" else 21,
            "gender": random.choice(["Male", "Female"]),
            "blood_group": random.choice(blood_groups),
            "profile_picture": f"{patient_name.lower()}.jpg",
            "medical_history": [
                {
                    "date": (datetime.now() - timedelta(days=random.randint(1, 10))).strftime("%Y-%m-%d"),
                    "description": random.choice(diseases)
                }
            ]
        }
        patients.append(patient)

        # Intake form
        intake_forms.append({
            "form_id": f"form{i+1}",
            "patient_id": patient_id,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "vital_signs": {
                "blood_pressure": f"{random.randint(100, 130)}/{random.randint(70, 90)}",
                "temperature": f"{random.uniform(97.0, 99.5):.1f}",
                "pulse": random.randint(60, 100)
            }
        })

        # 1-2 appointments
        for j in range(random.randint(1, 2)):
            appointments.append({
                "appointment_id": f"app{i*2+j+1}",
                "patient_id": patient_id,
                "doctor_id": f"doc{(i % 5) + 1}",
                "date": (datetime.now() + timedelta(days=random.randint(1, 7))).strftime("%Y-%m-%d"),
                "time": f"{random.randint(9,16)}:{random.choice(['00', '30'])}",
                "status": random.choice(["Scheduled", "Completed", "Cancelled"])
            })

        # 1-2 prescriptions
        for j in range(random.randint(1, 2)):
            prescriptions.append({
                "prescription_id": f"presc{i*2+j+1}",
                "patient_id": patient_id,
                "doctor_id": f"doc{(i % 5) + 1}",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "medicine": random.choice(medicines),
                "dosage": f"{random.randint(1,2)} tablets",
                "frequency": random.choice(["Once a day", "Twice a day"]),
                "duration": f"{random.randint(3,10)} days",
                "notes": "Take after meals"
            })

        # 1-2 pathology reports
        for j in range(random.randint(1, 2)):
            pathology_reports.append({
                "report_id": f"rep{i*2+j+1}",
                "patient_id": patient_id,
                "date": (datetime.now() - timedelta(days=random.randint(1, 5))).strftime("%Y-%m-%d"),
                "test_name": random.choice(tests),
                "status": random.choice(statuses),
                "diagnosis": random.choice(diagnoses)
            })

    # Insert all data
    patients_collection.insert_many(patients)
    intake_collections.insert_many(intake_forms)
    appointments_collection.insert_many(appointments)
    prescription_collection.insert_many(prescriptions)
    pathology_collection.insert_many(pathology_reports)

    print("✅ Structured sample data inserted successfully for all patients.")

except PyMongoError as e:
    print("❌ MongoDB Error:", e)
except Exception as e:
    print("❌ General Error:", e)
