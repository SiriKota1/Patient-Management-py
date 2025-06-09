import patient

while True:

    print("\n|--------------------------------------[ Patient Details Manager ]--------------------------------------|\n"
        "Please select one of the following options:\n"
        "Click '1' to add a patient\n"
        "Click '2' to print the list of patients\n"
        "Click '3' to get patient details\n"
        "Click '4' to update a patient's details\n"
        "Click '5' to remove a patient\n"
        "Click 'x' to exit\n")

    option = input("Enter your choice here --> ")
    match option:
        case "1":
            name = input("Enter patient name --> ")
            record_no = input("Enter patient record number --> ") #eg: P365
            blood_type = input("Enter patient blood type --> ")
            hospital_name = input("Enter hospital name --> ")
            print("\n")
            print(patient.add_patient(name, record_no, blood_type, hospital_name))

        case "2":
            print(patient.print_patient_list())

        case "3":
            record_no = input("Enter patient record number to get patient details: ")
            print(patient.get_patient(record_no))

        case "4":
            record_no = input("Enter patient record number to update patient details: ")
            print("Press 'a' to update patient name\n"
            "Press 'b' to update patient blood_type\n" 
            "Press 'c' to update hospital name\n")
            choice = input("Please enter your choice here: ")
            print(patient.update_patient(record_no, choice))

        case "5":
            record_no = input("Enter patient record number to delete patient: ")
            print(patient.delete_patient(record_no))

        case "x":
            print("Exiting patient manager...")
            break

        case _:
            print("You've entered an invalid choice!! Please enter the correct choice again...")
