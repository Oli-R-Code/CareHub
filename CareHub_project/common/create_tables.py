from common.database import *

# Main function to create all tables
def create_tables():
    conn = connect_db()
    if not conn:
        return

    cursor = conn.cursor()

    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS specialities (
            specialityID INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS doctors (
            doctorID INT AUTO_INCREMENT PRIMARY KEY,
            doctor_name VARCHAR(100) NOT NULL,
            specialityID INT,
            working_hours VARCHAR(255),
            FOREIGN KEY (specialityID) REFERENCES specialities(specialityID)
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            systemID INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            userID VARCHAR(100) UNIQUE NOT NULL,
            dob DATE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )""")
        

        cursor.execute("""CREATE TABLE IF NOT EXISTS availability (
            availabilityID INT AUTO_INCREMENT PRIMARY KEY,
            doctorID INT,
            availableDate DATE NOT NULL,
            availableTime TIME NOT NULL,
            isBooked BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (doctorID) REFERENCES doctors(doctorID)
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS appointments (
            appointmentID INT AUTO_INCREMENT PRIMARY KEY,
            userID VARCHAR(50),
            doctorID INT,
            appointmentDate DATE,
            appointmentTime TIME,
            status VARCHAR(20),
            FOREIGN KEY (userID) REFERENCES users(userID),
            FOREIGN KEY (doctorID) REFERENCES doctors(doctorID)
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS doctor_schedule (
            doctorID INT PRIMARY KEY,
            start_hour TIME NOT NULL,
            end_hour TIME NOT NULL,
            off_days VARCHAR(255),
            FOREIGN KEY (doctorID) REFERENCES doctors(doctorID)
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS admins (
            systemID INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            adminID VARCHAR(100) UNIQUE NOT NULL,
            dob DATE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS appointments_history (
            appointmentID INT PRIMARY KEY AUTO_INCREMENT,
            userID INT,
            doctorID INT,
            appointmentDate DATE,
            appointmentTime TIME,
            status VARCHAR(50),
            FOREIGN KEY (userID) REFERENCES users(systemID) ON DELETE CASCADE,
            FOREIGN KEY (doctorID) REFERENCES doctors(doctorID) ON DELETE CASCADE
        )""")


        conn.commit()
        print("All tables created successfully.")
    except mysql.connector.Error as err:
        print(f"Error while creating tables: {err}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_tables()