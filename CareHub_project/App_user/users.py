from common.database import *

class User:
    def __init__(self, systemID, full_name, userID, dob, email, password):
        """
        This is the 'constructor'
        'self' refers to the current object being created.
        The parameters correspond to the fields in 'users' table.
        """
        self.systemID = systemID
        self.full_name = full_name
        self.userID = userID
        self.dob = dob
        self.email = email
        self.password = password

    def __str__(self):
        """
        It defines how the object is printed.
        when calling 'print(user)', this is what will be shown.
        Useful for debugging or logging.
        """
        return f"User({self.full_name}, {self.email})"

    @classmethod
    def from_row(cls, row):
        """
        Creates a User object from a tuple or list (like a row fetched from a database).
        'cls' refers to the class itself, not a specific object.

        Example:
            row = (1, "Juno Mori", "33555876", "2000-04-02", "juno@example.com", "secure123")
            user = User.from_row(row)
        """
        return cls(*row)  # Unpacks the row tuple into constructor arguments

    def save_to_db(self):
        """
        Saves the current User object to the database.
        It executes an INSERT query using the user's information.
        """
        db = connect_db()
        cursor = db.cursor()

        sql = """
            INSERT INTO users (full_name, userID, dob, email, password)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            self.full_name,
            self.userID,
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
    def get_user_by_email(cls, email):
        """
        Searches the database for a user with the given email.
        If found, it returns a User object.
        If not, it returns None.
        """
        db = connect_db()
        cursor = db.cursor()

        sql = "SELECT * FROM users WHERE email = %s"
        cursor.execute(sql, (email,))
        row = cursor.fetchone()

        cursor.close()
        db.close()

        if row:
            return cls.from_row(row)
        else:
            print("No user found with that email.")
            return None