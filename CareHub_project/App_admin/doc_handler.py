from common.database import *

def doc_handler():
    while True:
        choice = input("""Please choose an operation:
A) List all doctors
B) Add a new doctor
C) Remove a doctor
D) Go back
""")
        match choice.upper():
            case 'A':
                list_doctors()
            case 'B':
                add_new_doctor()
            case 'C':
                remove_doctor()
            case 'D':
                return  # Go back to the previous menu
            case _:
                print("Invalid choice. Please try again.")

# List all doctors
def list_doctors():
    doctors = get_all_doctors()  # Assuming you have a function to fetch doctors
    if not doctors:
        print("No doctors found.")
        return

    print("List of all doctors:")
    for doctor in doctors:
        print(f"Doctor ID: {doctor['doctorID']}, Name: {doctor['full_name']}, Speciality: {doctor['specialityID']}")

# Add a new doctor
def add_new_doctor():
    doctor_name = input("Enter the doctor's full name: ")
    speciality_id = input("Enter the speciality ID: ")
    
    if not speciality_id.isdigit():
        print("Invalid speciality ID. Please enter a valid number.")
        return

    speciality_id = int(speciality_id)

    create_doctor(doctor_name, speciality_id)
    print(f"Doctor {doctor_name} added successfully.")

# Remove a doctor
def remove_doctor():
    doctor_id = input("Enter the doctor ID to remove: ")

    if not doctor_id.isdigit():
        print("Invalid doctor ID. Please enter a valid number.")
        return

    doctor_id = int(doctor_id)
    delete_doctor(doctor_id)
    print(f"Doctor with ID {doctor_id} has been removed.")


if __name__ == "__main__":
    pass