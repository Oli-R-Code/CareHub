from common.database import *
from App_user.appointments import * 

def app_handler(user_id):  
    while True:
        choice = input("""Please select an option:
A) Book an appointment
E) Check appointment status
F) View past appointments
G) Log out
Enter your choice: """).strip().upper()

        match choice:
            case 'A':
                select_speciality_and_doctor(user_id)
            case 'E':
                check_appointment_status(user_id)
            case 'F':
                view_past_appointments(user_id)
            case 'G':
                print("Logging out...")
                break
            case _:
                print("Invalid option. Please try again.")


def select_speciality_and_doctor(user_id):
    specialities = get_all_specialities()
    if not specialities:
        print("No specialities found in the system.")
        return

    description_map = {
        "A": """General Practitioner
If this is your first appointment with us, we recommend starting here! The General Practitioner (GP) is your first point of contact for most medical concerns. They can refer you to specialists if needed.""",

        "B": """Cardiology
For issues related to your heart or blood vessels. Cardiologists specialize in diagnosing and treating heart conditions.""",

        "C": """Gynecology
For reproductive and menstrual health, pregnancy care, and related concerns.""",

        "D": """Pediatrics
For children's health, from infancy through adolescence. Pediatricians specialize in the care and treatment of young patients."""
    }

    letter_keys = list(description_map.keys())

    print("Please select a speciality:\n")

    for i, spec in enumerate(specialities):
        if i < len(letter_keys):
            key = letter_keys[i]
            print(f"{key}) {description_map[key]}\n")
        else:
            print(f"{i+1}) {spec['name']}\n   {spec['description']}\n")

    print("F) Back to main menu")

    choice = input("Enter your choice: ").strip().upper()

    if choice == 'F':
        return

    if choice in letter_keys:
        index = letter_keys.index(choice)
    elif choice.isdigit():
        index = int(choice) - 1
    else:
        print("Invalid choice.")
        return

    if 0 <= index < len(specialities):
        selected = specialities[index]
        specialityID = selected['specialityID']
        print(f"You selected: {selected['name']}")

        doctors = get_doctors_by_speciality(specialityID)
        if not doctors:
            print("No doctors available for this speciality.")
            return

        print("Available doctors:")
        for i, doc in enumerate(doctors, start=1):
            print(f"{i}) {doc['doctor_name']} (Hours: {doc['working_hours']})")

        doctor_choice = input("Select a doctor by number or enter 'F' to go back: ").strip().upper()

        if doctor_choice == 'F':
            return

        if doctor_choice.isdigit():
            doctor_index = int(doctor_choice) - 1
            if 0 <= doctor_index < len(doctors):
                selected_doctor = doctors[doctor_index]
                print(f"\nYou selected: Dr. {selected_doctor['doctor_name']}")

                # Now call the appointment booking process
                #show_available_slots(selected_doctor['doctorID'],)
                book_appointment_flow(user_id, selected_doctor['doctorID'])

            else:
                print("Invalid doctor choice.")
        else:
            print("Invalid input. Please enter a number.")
    else:
        print("Invalid option.")

def check_appointment_status(user_id):
    query = """
        SELECT a.appointmentDate, a.appointmentTime, a.status, d.doctor_name AS doctor_name
        FROM appointments a
        JOIN doctors d ON a.doctorID = d.doctorID
        WHERE a.userID = %s AND a.status IN ('pending', 'confirmed')
        ORDER BY a.appointmentDate, a.appointmentTime;
    """
    params = (user_id,)
    results = execute_select(query, params)

    if not results:
        print("\nYou have no upcoming appointments.")
        return

    print("\nYour upcoming appointments:\n")
    for appt in results:
        date, time, status, doctor = appt['appointmentDate'], appt['appointmentTime'], appt['status'], appt['doctor_name']
        print(f"{date} at {time} with Dr. {doctor} → Status: {status.capitalize()}")

    input("\nPress Enter to return to the main menu...")

def view_past_appointments(user_id):
    query = """
        SELECT appointmentID, doctorID, appointmentDate, appointmentTime, status
        FROM appointments_history
        WHERE userID = %s
        ORDER BY appointmentDate DESC, appointmentTime DESC;
    """
    past_appointments = execute_select(query, (user_id,))
    
    if past_appointments:
        print("\nYour past appointments:\n")
        doctors = get_doctors()  # Get all doctors in one go
        for appointment in past_appointments:
            doctor_name = None
            for doctor in doctors:  # Loop through doctors to find the right one
                if doctor['doctorID'] == appointment['doctorID']:
                    doctor_name = doctor['doctor_name']
                    break  # Stop the loop once we find the correct doctor
            if doctor_name:
                print(f"Appointment ID: {appointment['appointmentID']}")
                print(f"Doctor: Dr. {doctor_name}")
                print(f"Date: {appointment['appointmentDate']}")
                print(f"Time: {appointment['appointmentTime']}")
                print(f"Status: {appointment['status']}\n")
            else:
                print(f"Appointment ID: {appointment['appointmentID']}")
                print(f"Doctor: [Doctor Not Found]")
                print(f"Date: {appointment['appointmentDate']}")
                print(f"Time: {appointment['appointmentTime']}")
                print(f"Status: {appointment['status']}\n")
    else:
        print("You have no past appointments.")

if __name__ == "__main__":
    app_handler()