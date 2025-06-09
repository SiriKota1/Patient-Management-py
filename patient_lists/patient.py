class Patient:
    def __init__(self, name: str, record_no: int, blood_type: str, hospital_name: str):
        self.name = name
        self.record_no = record_no
        self.blood_type = blood_type
        self.hospital_name = hospital_name
    
    def __repr__(self):
        return f"Patient(name = {self.name}, record_no = {self.record_no}, blood_type = {self.blood_type}, hospital_name = {self.hospital_name})"
    
patient_list = []

# add/create
# list
# get
# update
# delete/remove

# 1st func: Add/Create patient
def add_patient(name: str, record_no: str, blood_type: str, hospital_name: str):
    patient = Patient(name, record_no, blood_type, hospital_name)
    patient_list.append(patient)
    return patient

# 2nd func: Print the full list of patients
def print_patient_list():
    return patient_list

# 3rd func: Get patient data based on patient record number
def get_patient(record_no: str):
    for patient in patient_list:
        if patient.record_no == record_no:
                return patient
        
    print("Patient details not found...")

# 4th func: Update specific patient details based on patient record number and choice entered
def update_patient(record_no: str, choice):
    patient = get_patient(record_no)
    match choice:
        case "a":
            patient.name = input("Please enter new name: ")
        case "b":
            patient.blood_type = input("Please enter the blood type: ")
        case "c":
            patient.hospital_name = input("Please enter the new hospital name: ")   
        case _:
            print("Wrong choice!!")
    return patient

# 5th func: Delete a patient based on patient record no.
def delete_patient(record_no: str):
        patient = get_patient(record_no)
        patient_list.remove(patient)   
        print("Patient has been deleted...")
        return patient_list        
