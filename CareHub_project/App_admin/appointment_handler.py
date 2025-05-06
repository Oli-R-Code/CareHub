from common.database import get_pending_appointments, update_appointment_status, get_doctors
from common.send_email import *

def appointment_handler():
    print("\n--- Pending Appointment Requests ---\n")

    # Fetch doctors for filtering
    doctors = get_doctors()

    # Filter by doctor
    doctor_filter = input("Filter by doctor (or press Enter to skip):\n")
    if doctor_filter:
        filtered_doctors = [doc for doc in doctors if doc['doctor_name'].lower() == doctor_filter.lower()]
        if not filtered_doctors:
            print("No doctors found with that name. Showing all requests.\n")
            doctor_filter = None
    else:
        filtered_doctors = doctors
        print("No doctor filter applied. Showing all requests.\n")

    # Filter by date
    date_filter = input("Filter by date (YYYY-MM-DD) (or press Enter to skip):\n")
    
    # Retrieve and filter appointment requests based on filters
    requests = get_pending_appointments(doctor_filter, date_filter)
    #print("DEBUG requests:", requests) 


    if not requests:
        print("No pending appointments.\n")
        return

    # Display the filtered requests
    for req in requests:
        print(f"""
Appointment ID: {req['appointmentID']}
Patient      : {req['patient_name']}
Doctor       : {req['doctor_name']}
Date         : {req['appointmentDate']}
Time         : {req['appointmentTime']}
Status       : {req['status']}
        """)

        while True:
            choice = input("""Choose an action: 
A) Approve  
D) Deny  
S) Skip""")
            match choice.upper():
                case 'A':
                    update_appointment_status(req['appointmentID'], 'Confirmed')
                    print("Appointment confirmed.")
                    #print("DEBUG req contents:", req)
                    #print("DEBUG req keys:", list(req.keys()))
                    appointment_details = {
                        'user_id': req['user_id'],
                        'doctor_id': req['doctor_id'],
                        'date': req['appointmentDate'],
                        'time': req['appointmentTime'],
                        'status': 'Confirmed'
                    }
                    notify_user_of_appointment_status(appointment_details['user_id'], appointment_details['status'])
                    break
                case 'D':
                    update_appointment_status(req['appointmentID'], 'Denied')
                    print("Appointment denied.")
                    appointment_details = {
                        'user_id': req['user_id'],
                        'doctor_id': req['doctor_id'],
                        'date': req['appointmentDate'],
                        'time': req['appointmentTime'],
                        'status': 'Confirmed'
                    }
                    notify_user_of_appointment_status(appointment_details['user_id'], appointment_details['status'])
                    break
                case 'S':
                    print("Skipped.")
                    break
                case _:
                    print("Invalid option. Please choose A, D, or S.")

if __name__ == "__main__":
    appointment_handler()
