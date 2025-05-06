from datetime import datetime, timedelta
from common.database import *


def availability_handler():
    try:
        doctor_id = input("Enter the doctor ID: ").strip()
        start_date = input("Enter the start date (YYYY-MM-DD): ").strip()
        end_date = input("Enter the end date (YYYY-MM-DD): ").strip()

        weekdays_input = input("Enter weekdays as comma-separated numbers (0=Mon to 6=Sun): ").strip()
        weekdays = [int(day.strip()) for day in weekdays_input.split(",")]

        start_time = input("Enter daily start time (HH:MM): ").strip()
        end_time = input("Enter daily end time (HH:MM): ").strip()
        interval = int(input("Enter interval in minutes (e.g., 30): ").strip())

        add_bulk_availability(doctor_id, start_date, end_date, weekdays, start_time, end_time, interval)

    except Exception as e:
        print(f"An error occurred: {e}")


def add_bulk_availability(doctor_id, start_date_str, end_date_str, weekdays, start_time_str, end_time_str, interval_minutes):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    start_time = datetime.strptime(start_time_str, "%H:%M").time()
    end_time = datetime.strptime(end_time_str, "%H:%M").time()

    current_date = start_date
    slots = []

    while current_date <= end_date:
        if current_date.weekday() in weekdays:  # 0 = Monday, ..., 6 = Sunday
            slot_time = datetime.combine(current_date, start_time)
            end_datetime = datetime.combine(current_date, end_time)

            while slot_time < end_datetime:
                slots.append((doctor_id, slot_time.date(), slot_time.time(), False))
                slot_time += timedelta(minutes=interval_minutes)
        current_date += timedelta(days=1)

    # Insert all generated slots into the database
    query = "INSERT INTO availability (doctorID, availableDate, availableTime, isBooked) VALUES (%s, %s, %s, %s)"
    for slot in slots:
        execute_non_select(query, slot)

    print(f"{len(slots)} availability slots added for doctor {doctor_id}.")
