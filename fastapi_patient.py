import uvicorn
from fastapi import FastAPI
import mysql.connector

app = FastAPI()

class Patient:
    def __init__(self, name: str, record_no: int, blood_type: str, hospital_name: str):
        self.name = name
        self.record_no = record_no
        self.blood_type = blood_type
        self.hospital_name = hospital_name
    
    def __repr__(self):
        return f"Patient(name = {self.name}, record_no = {self.record_no}, blood_type = {self.blood_type}, hospital_name = {self.hospital_name})"
    
patient_list = []
db = mysql.connector.connect(
     host="localhost",
     user="root",
     password="Siri@2005",
     database="patientDB"
)

mycursor = db.cursor()
'Uncomment the following line to create and print the database and table'
'-----------------------------------------------------------------------------------------------------------------------------------------------------------------'
# mycursor.execute("CREATE DATABASE patientDB")
# print(db)

# mycursor.execute("CREATE TABLE patientdata(name VARCHAR(255), record_no VARCHAR(255) PRIMARY KEY, blood_type VARCHAR(255), hospital_name VARCHAR(255))")
# mycursor.execute("SHOW TABLES")

# for x in mycursor:
#   print(x)
'-----------------------------------------------------------------------------------------------------------------------------------------------------------------'


@app.get("/") # Endpoint or RestAPI endpoint
def read_root():
    return {"message": "Welcome to the Patient Management API"}

# add/create
# list
# get
# update
# delete/remove

# 1st func: Add/Create patient
@app.post("/create-patient/")
def add_patient(name: str, record_no: str, blood_type: str, hospital_name: str):
    sql = "INSERT INTO patientdata (name, record_no, blood_type, hospital_name) VALUES (%s, %s, %s, %s)"
    val = (name, record_no, blood_type, hospital_name)
    mycursor.execute(sql, val)
    db.commit()
    mycursor.execure("SELECT * FROM patientdata WHERE record_no = %s", (record_no,))
    new_patient = mycursor.fetchall()
    return new_patient

# 2nd func: Print the full list of patients
@app.get("/print-patient-list/")
def print_patient_list():
    mycursor.execute("SELECT * FROM patientdata")
    all_patients = mycursor.fetchall()
    return all_patients
    

# 3rd func: Get patient data based on patient record number
@app.get("/print-patient-details/{record_no}")
def get_patient(record_no: str):
    # for patient in patient_list:
    #     if patient.record_no == record_no:
    #             return patient    
    # print("Patient details not found...")
    mycursor.execure("SELECT * FROM patientdata WHERE record_no = %s", (record_no,))
    result = mycursor.fetchall()
    return result

# 4th func: Update specific patient details based on patient record number and choice entered
@app.patch("/update-patient-details/{record_no}")
def update_patient(record_no: str, name:str=None, blood_type:str=None, hospital_name:str=None):
    patient = get_patient(record_no)
    if not patient:
        return {"message": "Patient not found"}
    if name:
        sql = "UPDATE patientdata SET name = %s WHERE record_no = %s"
        val = (name, record_no)
        mycursor.execute(sql, val)
        db.commit()
    if blood_type:
        sql = "UPDATE patientdata SET blood_type = %s WHERE record_no = %s"
        val = (blood_type, record_no)
        mycursor.execute(sql, val)
        db.commit()
    if hospital_name:
        sql = "UPDATE patientdata SET hospital_name = %s WHERE record_no = %s"
        val = (hospital_name, record_no)
        mycursor.execute(sql, val)
        db.commit()
    mycursor.execute("SELECT * FROM patientdata WHERE record_no = %s",(record_no,))
    updated_patient_details = mycursor.fetchall()
    return updated_patient_details

# 5th func: Delete a patient based on patient record no.
@app.delete("/delete-patient/{record_no}")
def delete_patient(record_no: str):
    mycursor.execute("DELETE FROM patientdata WHERE record_no = %s", (record_no,))       
    db.commit()
    return {"message": "Patient deleted successfully"}
