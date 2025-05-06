import mysql.connector
import re

def connect_db():
    try:
        my_db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="carehub"
        )
        if my_db.is_connected():
            #print("db connected")
            return my_db
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Reusable function for executing SELECT queries
def execute_select(query, params=None):
    conn = connect_db()
    if not conn:
        return None

    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# Reusable function for executing INSERT, UPDATE, DELETE queries
def execute_non_select(query, params=None):
    conn = connect_db()
    if not conn:
        return None

    cursor = conn.cursor()
    cursor.execute(query, params or ())
    conn.commit()
    cursor.close()
    conn.close()

def user_id_exists(userID):
    query = "SELECT * FROM users WHERE userID = %s"
    result = execute_select(query, (userID,))
    return len(result) > 0

def admin_id_exists(adminID):
    query = "SELECT * FROM admins WHERE adminID = %s"
    result = execute_select(query, (adminID,))
    return len(result) > 0

def email_exists(email):
    query = "SELECT * FROM users WHERE email = %s"
    result = execute_select(query, (email,))
    return len(result) > 0

def admin_email_exists(email):
    query = "SELECT * FROM admins WHERE email = %s"
    result = execute_select(query, (email,))
    return len(result) > 0

def get_admin_emails():
    query = "SELECT email FROM admins"
    results = execute_select(query)
    return [row['email'] for row in results] if results else []  

# Fetch the user's email by user ID
def get_user_email(userID):
    query = "SELECT email FROM users WHERE userID = %s"
    result = execute_select(query, (userID,))
    if result:
        return result[0]["email"]
    else:
        print(f"[WARN] No user email found for ID: {userID}")
        return None




def admin_first_code_exists(adminID):
    query = "SELECT COUNT(*) FROM admin_first_code WHERE admin_code = %s"
    result = execute_select(query, (adminID,))
    return result[0]['COUNT(*)'] > 0  # Returns True if admin code exists, False otherwise

def remove_admin_first_code(adminID):
    query = "DELETE FROM admin_first_code WHERE admin_code = %s"
    execute_non_select(query, (adminID,))

def get_all_specialities():
    query = "SELECT specialityID, name FROM specialities"
    return execute_select(query)

def get_doctors_by_speciality(specialityID):
    query = """
        SELECT doctorID, doctor_name, specialityID, working_hours
        FROM doctors
        WHERE specialityID = %s
    """
    return execute_select(query, (specialityID,))

def get_available_slots_db(doctor_id, date=None):
    if date:
        query = """
            SELECT * FROM availability 
            WHERE doctorID = %s AND availableDate = %s AND isBooked = FALSE
            ORDER BY availableDate, availableTime
        """
        params = (doctor_id, date)
    else:
        query = """
            SELECT * FROM availability 
            WHERE doctorID = %s AND isBooked = FALSE
            ORDER BY availableDate, availableTime
        """
        params = (doctor_id,)
    
    return execute_select(query, params)

def get_slot_details(availability_id, doctor_id):
    query = """
        SELECT availableDate, availableTime
        FROM availability
        WHERE availabilityID = %s AND doctorID = %s AND isBooked = FALSE
    """
    result = execute_select(query, (availability_id, doctor_id))
    if result:
        # Return the date and time as a tuple
        return result[0]['availableDate'], result[0]['availableTime']
    return None

def insert_appointment(user_id, doctor_id, date, time):
    query = """
        INSERT INTO appointments (userID, doctorID, appointmentDate, appointmentTime, status)
        VALUES (%s, %s, %s, %s, 'pending')
    """
    execute_non_select(query, (user_id, doctor_id, date, time))

def mark_slot_as_booked(availability_id):
    query = "UPDATE availability SET isBooked = TRUE WHERE availabilityID = %s"
    execute_non_select(query, (availability_id,))

def get_pending_appointments(doctor_name=None, appointment_date=None):
    query = """
    SELECT 
        appointmentID,
        userID AS user_id,
        doctorID AS doctor_id,
        appointmentDate AS date,
        appointmentTime AS time,
        status
    FROM appointments
    WHERE status = 'Pending'
"""

    filters = []
    params = []

    if doctor_name:
        query += " AND d.name = %s"
        filters.append(doctor_name)

    if appointment_date:
        query += " AND a.appointmentDate = %s"
        filters.append(appointment_date)

    return execute_select(query, tuple(filters))

def get_all_doctors():
    query = """
        SELECT doctorID, doctor_name, specialityID
        FROM doctors
    """
    return execute_select(query)

def get_doctors():
    query = "SELECT doctorID, doctor_name FROM doctors"
    return execute_select(query)

def create_doctor(doctor_name, speciality_id):
    query = """
        INSERT INTO doctors (doctor_name, specialityID)
        VALUES (%s, %s)
    """
    execute_non_select(query, (doctor_name, speciality_id))

def create_availability(doctor_id, available_date, available_time):
    query = """
        INSERT INTO availability (doctorID, availableDate, availableTime, isBooked)
        VALUES (%s, %s, %s, FALSE)
    """
    execute_non_select(query, (doctor_id, available_date, available_time))

# Admin functions for adding/removing/editing doctors and availabilities
def update_doctor_working_hours(doctor_id, new_hours):
    query = """
        UPDATE doctors SET working_hours = %s WHERE doctorID = %s
    """
    execute_non_select(query, (new_hours, doctor_id))

def delete_doctor(doctor_id):
    query = "DELETE FROM doctors WHERE doctorID = %s"
    execute_non_select(query, (doctor_id,))

def delete_availability(availability_id):
    query = "DELETE FROM availability WHERE availabilityID = %s"
    execute_non_select(query, (availability_id,))

def get_doctor_schedule(doctor_id):
    query = "SELECT * FROM doctor_schedule WHERE doctorID = %s"
    return execute_select(query, (doctor_id,))

def upsert_doctor_schedule(doctor_id, start_hour, end_hour, off_days):
    query = """
        INSERT INTO doctor_schedule (doctorID, start_hour, end_hour, off_days)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        start_hour = VALUES(start_hour),
        end_hour = VALUES(end_hour),
        off_days = VALUES(off_days)
    """
    execute_non_select(query, (doctor_id, start_hour, end_hour, off_days))

def delete_doctor_schedule(doctor_id):
    query = "DELETE FROM doctor_schedule WHERE doctorID = %s"
    execute_non_select(query, (doctor_id,))


def add_speciality(name):
    query = "INSERT INTO specialities (name) VALUES (%s)"
    execute_non_select(query, (name,))

def remove_speciality(speciality_id):
    query = "DELETE FROM specialities WHERE specialityID = %s"
    execute_non_select(query, (speciality_id,))

def get_pending_appointments(doctor_filter, date_filter):
    query = """
        SELECT a.appointmentID,
        a.userID AS user_id,
        a.doctorID AS doctor_id,
        u.full_name AS patient_name,
        d.doctor_name AS doctor_name,
        a.appointmentDate,
        a.appointmentTime,
        a.status
        FROM appointments a
        JOIN users u ON a.userID = u.userID
        JOIN doctors d ON a.doctorID = d.doctorID
        WHERE a.status = 'Pending'
    """
    return execute_select(query)

def update_appointment_status(appointment_id, new_status):
    query = "UPDATE appointments SET status = %s WHERE appointmentID = %s"
    execute_non_select(query, (new_status, appointment_id))


