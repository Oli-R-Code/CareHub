from common.database import *
from App_user.users import *
from common.auth import password_check 

class users_auth:
    def __init__(self):
        self.user_id = None

    def sign_In(self):
        print("""Please enter your information. 
Be mindfull of spelling errors, as personal information can not be edited after sign in.
            """)
        full_name = input("Full name: ")
        
        while True:
            userID = input("Health insurance number/ID number: ")
            if user_id_exists(userID):
                print("That ID is already in use. Please enter a different one.")
            else:
                break

        dob = input("Date of birth (YYYY-MM-DD): ")

        while True:
            email = input("Email: ")
            if email_exists(email):
                print("That email is already registered. Please use another.")
            else:
                break

        while True:
            password = input("Enter a secure Password: ")
        
            if not password_check(password):
                print("""Password not valid. 
                        Must include at least 6 characters, 
                        at least one uppercase/lowercase, 
                        at least one number, 
                        at least one special character: _-+*?!$%#<>)""")
                continue
            
            confirmPassword = input("Re-enter password: ")

            if password != confirmPassword:
                print("Passwords don't match. Please try again.")
                continue

            print("Password successfully created.")
            break

        new_user = User(None, full_name, userID, dob, email, password)
        new_user.save_to_db()

        input("Press enter to return to the menu...")
        

    def logIn(self):
        userCheck = input("Please enter email: ")
        if email_exists(userCheck):
            passwordAttempt = input("Please enter your password: ")
            conn = connect_db()

            if not conn:
                print("Unable to connect. Please try again later.")
                return False
            
            cursor = conn.cursor()
            cursor.execute("SELECT userID, password, full_name FROM users WHERE email = %s", (userCheck,))
            result = cursor.fetchone()

            cursor.close()
            conn.close()
            if result:
                user_id, storedPassword, fullname = result

                if passwordAttempt == storedPassword:
                    print(f"Welcome, {fullname}!")
                    self.user_id = user_id  # Store user_id if login is successful
                    return self.user_id                
                else:
                    print("Incorrect password. Access denied.")
                    return False
            else:
                print("Unexpected error: user not found after checking existence.")
                return False
        else:
            print("No account found with that email.")
        return False





if __name__ == "__main__":
    pass