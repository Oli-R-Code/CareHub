from common.database import *

class Admin:
    def __init__(self, systemID, full_name, adminID, dob, email, password):
        #This is the constructor. 'self' refest to the current objetct being created
        
        self.systemID = systemID
        self.full_name = full_name
        self.adminID = adminID
        self.dob = dob
        self.email = email
        self.password = password
        
    def __str__(self):
        #The function fefines how the object is printed
        return f"Admin({self.full_name}, {self.email})"
    
    @classmethod
    def from_row(cls, row):
        """
        Creates a User object from a tuple or list (like a row fetched from a database).
        'cls' refers to the class itself, not a specific object.
        """
        return cls(*row)  # Unpacks the row tuple into constructor arguments

    def save_to_db(self):
        """
        Saves the current Admin object to the database.
        It executes an INSERT query using the user's information.
        """
        db = connect_db()
        cursor = db.cursor()

        sql = """
            INSERT INTO admins (full_name, adminID, dob, email, password)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            self.full_name,
            self.adminID,
            self.dob,
            self.email,
            self.password
        )

        try:
            cursor.execute(sql, values)
            db.commit()  # Saves the changes to the database
            print("User saved to database.")
        except mysql.connector.Error as err:
            print("Error while saving user:", err)
        finally:
            cursor.close()
            db.close()

    @classmethod
    def get_admin_by_email(cls, email):
        """
        Searches the database for a user with the given email.
        If found, it returns a User object.
        If not, it returns None.
        """
        db = connect_db()
        cursor = db.cursor()

        sql = "SELECT * FROM admins WHERE email = %s"
        cursor.execute(sql, (email,))
        row = cursor.fetchone()

        cursor.close()
        db.close()

        if row:
            return cls.from_row(row)
        else:
            print("No admin found with that email.")
            return None