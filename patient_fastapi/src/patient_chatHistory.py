import uvicorn
from fastapi import FastAPI
import mysql.connector
from pydantic import BaseModel
from ollama import chat
from ollama import ChatResponse



app = FastAPI()

class User(BaseModel):
    name: str=None
    record_no: str
    blood_type: str=None
    hospital_name: str=None

class UserUpdate(BaseModel):
    name: str
    blood_type: str
    hospital_name: str

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

# Create chat history table if it doesn't exist
mycursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question TEXT,
    response TEXT
)
""")
db.commit()

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
def add_patient(user: User):
    sql = "INSERT INTO patientdata (name, record_no, blood_type, hospital_name) VALUES (%s, %s, %s, %s)"
    val = (user.name, user.record_no, user.blood_type, user.hospital_name)
    mycursor.execute(sql, val)
    db.commit()
    mycursor.execute("SELECT * FROM patientdata WHERE record_no = %s", (user.record_no,))
    new_patient = mycursor.fetchall()
    # new_patient = fetchall_as_pydantic(cursor, User)
    user_list = []
    for patient in new_patient:
        user = {"name":patient[0], "record_no":patient[1], "blood_type":patient[2], "hospital_name":patient[3]}
        user_list.append(user)
    return user_list

# 2nd func: Print the full list of patients
@app.get("/print-patient-list/")
def print_patient_list():
    mycursor.execute("SELECT * FROM patientdata")
    all_patients = mycursor.fetchall()
    user_list = []
    for patient in all_patients:
        user = {"name":patient[0], "record_no":patient[1], "blood_type":patient[2], "hospital_name":patient[3]}
        user_list.append(user)
    return user_list
    

# 3rd func: Get patient data based on patient record number
@app.get("/print-patient-details/{record_no}")
def get_patient(record_no: str):
    # for patient in patient_list:
    #     if patient.record_no == record_no:
    #             return patient    
    # print("Patient details not found...")
    mycursor.execute("SELECT * FROM patientdata WHERE record_no = %s", (record_no,))
    result = mycursor.fetchall()
    user_list = []
    for patient in result:
        user = {"name":patient[0], "record_no":patient[1], "blood_type":patient[2], "hospital_name":patient[3]}
        user_list.append(user)
    return user_list

# 4th func: Update specific patient details based on patient record number and choice entered
@app.patch("/update-patient-details/{record_no}")
def update_patient(record_no: str, user: User):
    patient = get_patient(user.record_no)
    if not patient:
        return {"message": "Patient not found"}
    if user.name:
        sql = "UPDATE patientdata SET name = %s WHERE record_no = %s"
        val = (user.name, user.record_no)
        mycursor.execute(sql, val)
        db.commit()
    if user.blood_type:
        sql = "UPDATE patientdata SET blood_type = %s WHERE record_no = %s"
        val = (user.blood_type, user.record_no)
        mycursor.execute(sql, val)
        db.commit()
    if user.hospital_name:
        sql = "UPDATE patientdata SET hospital_name = %s WHERE record_no = %s"
        val = (user.hospital_name, user.record_no)
        mycursor.execute(sql, val)
        db.commit()
    mycursor.execute("SELECT * FROM patientdata WHERE record_no = %s",(user.record_no,))
    updated_patient_details = mycursor.fetchall()
    user_list = []
    for patient in updated_patient_details:
        user = {"name":patient[0], "record_no":patient[1], "blood_type":patient[2], "hospital_name":patient[3]}
        user_list.append(user)
    return user_list

# 5th func: Delete a patient based on patient record no.
@app.delete("/delete-patient/{record_no}")
def delete_patient(record_no: str):
    mycursor.execute("DELETE FROM patientdata WHERE record_no = %s", (record_no,))       
    db.commit()
    return {"message": "Patient deleted successfully"}

# ollama chat with chat history save to DB
@app.get("/ollama-chat/")
def ollama_chat(question:str):
    response: ChatResponse = chat(model='llama3.1:8b', messages=[
      {
        'role': 'user',
        'content': question,
      },
    ])
    print(response)
    print(response['message']['content'])
    # or access fields directly from the response object
    print(response.message.content)

    response_text = response.message.content
    sql = "INSERT INTO chat_history (question, response) VALUES (%s, %s)"
    val = (question, response_text)
    mycursor.execute(sql, val)
    db.commit()

    return {"chat_response":response_text}

# New endpoint: Get full chat history
@app.get("/chat-history/")
def chat_history():
    mycursor.execute("SELECT * FROM chat_history ORDER BY id DESC")
    history = mycursor.fetchall()
    history_list = []
    for h in history:
        chat = {"question": h[1], "response": h[2]}
        history_list.append(chat)
    return history_list

# Optional: Clear chat history
@app.delete("/delete-chat-history/")
def delete_chat_history():
    mycursor.execute("DELETE FROM chat_history")
    db.commit()
    return {"message": "Chat history cleared"}
