from common.database import *

def sch_handler():
    while True:
        choice = input("""
Please choose a scheduling operation:
A) View all doctor schedules
B) Add a new schedule
C) Edit a schedule
D) Remove a schedule
E) Return to main menu
""")
        match choice.upper():
            case 'A':
                list_doctor_schedules()
            case 'B':
                add_doctor_schedule()
            case 'C':
                edit_doctor_schedule()
            case 'D':
                remove_doctor_schedule()
            case 'E':
                break
            case _:
                print("Invalid option. Please try again.")


def list_doctor_schedules():
    query = """
        SELECT d.doctorID, d.full_name, s.start_hour, s.end_hour, s.off_days
        FROM doctor_schedule s
        JOIN doctors d ON s.doctorID = d.doctorID
    """
    results = execute_select(query)

    if not results:
        print("No schedules found.")
        return

    print("\nDoctor Schedules:")
    for row in results:
        print(f"ID: {row['doctorID']} | Name: {row['full_name']}")
        print(f"  Working Hours: {row['start_hour']} to {row['end_hour']}")
        print(f"  Off Days: {row['off_days']}\n")


def add_doctor_schedule():
    doctor_id = input("Enter doctor ID: ")
    
    # Check if doctor exists
    doctor = execute_select("SELECT full_name FROM doctors WHERE doctorID = %s", (doctor_id,))
    if not doctor:
        print("Doctor not found.")
        return

    # Check if schedule already exists
    existing = execute_select("SELECT * FROM doctor_schedule WHERE doctorID = %s", (doctor_id,))
    if existing:
        print("Schedule already exists for this doctor.")
        return

    start_hour = input("Enter start hour (HH:MM): ")
    end_hour = input("Enter end hour (HH:MM): ")
    off_days = input("Enter off days (comma-separated, e.g., 'Tuesday,Saturday'): ")

    query = """
        INSERT INTO doctor_schedule (doctorID, start_hour, end_hour, off_days)
        VALUES (%s, %s, %s, %s)
    """
    execute_non_select(query, (doctor_id, start_hour, end_hour, off_days))
    print("Schedule added successfully.")

def edit_doctor_schedule():
    doctor_id = input("Enter doctor ID to edit: ")

    existing = execute_select("SELECT * FROM doctor_schedule WHERE doctorID = %s", (doctor_id,))
    if not existing:
        print("No schedule found for this doctor.")
        return

    print("Leave input blank to keep current value.")

    start_hour = input(f"New start hour (current: {existing[0]['start_hour']}): ") or existing[0]['start_hour']
    end_hour = input(f"New end hour (current: {existing[0]['end_hour']}): ") or existing[0]['end_hour']
    off_days = input(f"New off days (current: {existing[0]['off_days']}): ") or existing[0]['off_days']

    query = """
        UPDATE doctor_schedule
        SET start_hour = %s, end_hour = %s, off_days = %s
        WHERE doctorID = %s
    """
    execute_non_select(query, (start_hour, end_hour, off_days, doctor_id))
    print("Schedule updated successfully.")

def remove_doctor_schedule():
    doctor_id = input("Enter doctor ID to remove schedule: ")

    existing = execute_select("SELECT * FROM doctor_schedule WHERE doctorID = %s", (doctor_id,))
    if not existing:
        print("No schedule found for this doctor.")
        return

    confirm = input("Are you sure you want to delete this schedule? (y/n): ")
    if confirm.lower() != 'y':
        print("Cancelled.")
        return

    query = "DELETE FROM doctor_schedule WHERE doctorID = %s"
    execute_non_select(query, (doctor_id,))
    print("Schedule removed.")

if __name__ == "__main__":
    sch_handler()