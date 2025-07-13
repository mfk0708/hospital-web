from database import (
    patients_collection,
    appointments_collection,
    doctors_collection,
    prescription_collection,
    pathology_collection,
    counter_collections,
    fs  # GridFS instance
)

from datetime import datetime, timedelta
import random
from pymongo.errors import PyMongoError
from pymongo import ReturnDocument
from bson import ObjectId

# --- Upload image and return ObjectId ---
def upload_image_and_get_id(file_path: str, filename: str):
    with open(file_path, "rb") as f:
        data = f.read()
    existing = fs.find_one({"filename": filename})
    if existing:
        fs.delete(existing._id)
    return fs.put(data, filename=filename)

# --- Helper to generate ordered custom IDs ---
def get_next_id(prefix: str) -> str:
    result = counter_collections.find_one_and_update(
        {"_id": prefix},
        {"$inc": {"sequence_value": 1}},
        return_document=ReturnDocument.AFTER,
        upsert=True
    )
    return f"{prefix}{result['sequence_value']}"

# Sample data pools
names = ["Fahad", "Mubarak", "Rifai", "Sheik", "Afrin", "Durga", "Rifqa", "Sathyasri", "Kaleel", "Nivetha"]
blood_groups = ["A +ve", "B +ve", "AB -ve", "O +ve", "A -ve"]
diseases = ["Fever", "Diabetes", "Hypertension", "Asthma", "Allergy"]
medicines = ["Paracetamol", "Metformin", "Cetirizine", "Amoxicillin", "Atorvastatin"]
tests = ["Blood Test", "X-Ray", "MRI", "ECG"]
statuses = ["Pending", "Completed", "In Progress"]
diagnoses = ["Normal", "Infection", "Deficiency", "Chronic Disease"]
specializations = ["General", "Cardiology", "ENT", "Dermatology", "Neurology"]
doctor_name = ['Vijay', 'Dhanush', 'Ajith', 'Rajini', 'Kamal']
cities = ["Chennai", "Coimbatore", "Madurai", "Tiruchirapalli", "Salem"]
streets = ["Main St", "2nd Cross Rd", "Park Ave", "North Street", "Lakeview Rd"]

try:
    # Clear existing collections
    patients_collection.delete_many({})
    doctors_collection.delete_many({})
    appointments_collection.delete_many({})
    prescription_collection.delete_many({})
    pathology_collection.delete_many({})
    counter_collections.delete_many({})  # Reset counters

    # Upload image once and get ObjectId
    image_id = upload_image_and_get_id("static/images/doc1.jpg", "doc1.jpg")

    # Insert doctors
    doctors = []
    for i in range(5):
        doctor_id = get_next_id("doc")
        doctor = {
            "doctor_id": doctor_id,
            "name": f"Dr. {doctor_name[i]}",
            "specialization": specializations[i],
            "phone": f"+91-98765{1000+i}",
            "image_file_id": image_id,  # Storing GridFS image ObjectId
            "pie": {
                "completedPercentage": random.randint(60, 100)
            },
            "bar": [
                {"day": "Mon", "hours": random.randint(4, 8)},
                {"day": "Tue", "hours": random.randint(4, 8)},
                {"day": "Wed", "hours": random.randint(4, 8)},
                {"day": "Thu", "hours": random.randint(4, 8)},
                {"day": "Fri", "hours": random.randint(4, 8)}
            ],
        }
        doctors.append(doctor)
    doctors_collection.insert_many(doctors)

    # Insert patients and related data
    patients = []
    appointments = []
    prescriptions = []
    pathology_reports = []

    for i in range(10):
        patient_id = get_next_id("pat")
        patient_name = names[i]
        dob = datetime.now() - timedelta(days=random.randint(18 * 365, 60 * 365))
        age = (datetime.now() - dob).days // 365

        city = random.choice(cities)
        address = f"{random.randint(10, 99)} {random.choice(streets)}, {city}"

        patient = {
            "patient_id": patient_id,
            "name": patient_name,
            "dob": dob.strftime("%Y-%m-%d"),
            "age": age,
            "gender": random.choice(["Male", "Female"]),
            "blood_group": random.choice(blood_groups),
            "weight": random.randint(50, 90),
            "height": random.randint(150, 190),
            "emergency_contact": f"+91-9{random.randint(100000000, 999999999)}",
            "phone": f"+91-8{random.randint(100000000, 999999999)}",
            "city": city,
            "address": address,
            "pincode": random.randint(600001, 699999),
            "assurance_number": f"INS{random.randint(100000, 999999)}",
            "registration_number": f"REG{random.randint(1000, 9999)}",
            "expiry_date": (datetime.now() + timedelta(days=random.randint(365, 3 * 365))).strftime("%Y-%m-%d"),
            "marital_status": random.choice(["Single", "Married"]),
            "email": f"{patient_name.lower()}@example.com",
            "registration_date": datetime.now().strftime("%Y-%m-%d"),
            "medical_history": [
                {
                    "date": (datetime.now() - timedelta(days=random.randint(1, 10))).strftime("%Y-%m-%d"),
                    "description": random.choice(diseases)
                }
            ],
            "intake_form": {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "vital_signs": {
                    "blood_pressure": f"{random.randint(100, 130)}/{random.randint(70, 90)}",
                    "temperature": f"{random.uniform(97.0, 99.5):.1f}",
                    "pulse": random.randint(60, 100)
                }
            },
            "hemoglobin": [
                { "month": "3 months ago", "value": round(random.uniform(11.5, 13.0), 1) },
                { "month": "2 months ago", "value": round(random.uniform(11.8, 13.5), 1) },
                { "month": "1 month ago", "value": round(random.uniform(12.0, 13.7), 1) },
                { "month": "Present", "value": round(random.uniform(12.5, 14.0), 1) }
            ]
        }

        patients.append(patient)

        # Appointments
        for j in range(random.randint(1, 2)):
            appointments.append({
                "appointment_id": get_next_id("apt"),
                "patient_id": patient_id,
                "doctor_id": f"doc{(i % 5) + 1}",
                "date": (datetime.now() + timedelta(days=random.randint(1, 7))).strftime("%Y-%m-%d"),
                "time": f"{random.randint(9,16)}:{random.choice(['00', '30'])}",
                "status": random.choice(["Scheduled", "Completed"])
            })

        # Prescriptions
        for j in range(random.randint(1, 2)):
            prescriptions.append({
                "prescription_id": get_next_id("presc"),
                "patient_id": patient_id,
                "doctor_id": f"doc{(i % 5) + 1}",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "medicine": random.choice(medicines),
                "dosage": f"{random.randint(1,2)} tablets",
                "frequency": random.choice(["Once a day", "Twice a day"]),
                "duration": f"{random.randint(3,10)} days",
                "notes": "Take after meals"
            })

        # Pathology Reports
        for j in range(random.randint(1, 2)):
            pathology_reports.append({
                "report_id": get_next_id("rep"),
                "patient_id": patient_id,
                "date": (datetime.now() - timedelta(days=random.randint(1, 5))).strftime("%Y-%m-%d"),
                "test_name": random.choice(tests),
                "status": random.choice(statuses),
                "test_result": random.choice(diagnoses)
            })

    # Insert all data
    patients_collection.insert_many(patients)
    appointments_collection.insert_many(appointments)
    prescription_collection.insert_many(prescriptions)
    pathology_collection.insert_many(pathology_reports)

    print("✅ Sample data with full patient & doctor records inserted successfully.")

except PyMongoError as e:
    print("❌ MongoDB Error:", e)
except Exception as e:
    print("❌ General Error:", e)
