import common.database as database
from common.send_email import *
from datetime import datetime


def show_available_slots(doctor_id):
    date_input = input("Enter date to view available slots (YYYY-MM-DD): ").strip()
    if not date_input:
        print("No date entered. No slots will be shown.")
        return None

    try:
        from datetime import datetime
        selected_date = datetime.strptime(date_input, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please enter in YYYY-MM-DD format.")
        return None

    slots = database.get_available_slots_db(doctor_id, selected_date)

    if not slots:
        print("No available slots for this doctor on that date.")
        return None

    print(f"\nAvailable slots for {selected_date}:")
    for i, slot in enumerate(slots):
        print(f"{i + 1}) {slot['availableTime']}")
    return slots



def book_appointment_flow(user_id, doctor_id):
    # Show available slots for the doctor
    slots = show_available_slots(doctor_id)
    if not slots:
        print("No available slots found.")
        return

    try:
        choice = int(input("Select a slot number: ").strip()) - 1
        if 0 <= choice < len(slots):
            selected = slots[choice]
            availability_id = selected['availabilityID']

            # Fetch slot details to get the correct date and time
            slot_details = database.get_slot_details(availability_id, doctor_id)
            if not slot_details:
                print("That slot is no longer available.")
                return

            # Unpack date and time
            date, time = slot_details
            if not date or not time:
                print("Invalid date or time for the selected slot.")
                return

            # Insert the appointment with the fetched date and time
            database.insert_appointment(user_id, doctor_id, date, time)

            # Mark the slot as booked
            database.mark_slot_as_booked(availability_id)

            print("Appointment successfully requested (status: pending).")

            # Notify the admin of the pending appointment
            appointment_details = {
                'user_id': user_id,
                'doctor_id': doctor_id,
                'date': date,
                'time': time
            }
            notify_admin_of_pending_request(appointment_details)
            
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")


if __name__ == "__main__":
    pass