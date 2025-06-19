import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME1")]

patients_collection = db["Patients"]
appointments_collection = db["Appointment"]
doctors_collection = db["Doctor"]
pathology_collection=db['Pathology_reports']
prescription_collection=db['Prescriptions']
intake_collections=db['Intake_forms']
counter_collections=db["Counter"]

 
