from common.database import *
from App_admin.admins import *
from common.auth import password_check

class admin_auth:
    def sign_In(self):
        print("Please enter your information.")
        full_name = input("Full name: ")
        
        while True:
            adminID = input("Admin ID number: ")
            
            # Check if the adminID exists in admin_first_code table
            if admin_first_code_exists(adminID):
                # If it exists in admin_first_code, accept it and remove it from the table
                print("Admin ID accepted from first-time code.")
                remove_admin_first_code(adminID)  # Remove from admin_first_code after accepting

                break  # Proceed to next step since we have a valid adminID

            # If it's already in the admins table, don't allow it
            elif admin_id_exists(adminID):
                print("That ID is already in use. Please enter a different one or go back to login")
            
            else:
                print("That ID does not exist. Please enter a valid ID or go back.")
                break  # End the loop if not found in both places

        dob = input("Date of birth (YYYY-MM-DD): ")

        while True:
            email = input("Email: ")
            if admin_email_exists(email):
                print("This email is already registered. Please use another or go back to login.")
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

        new_admin = Admin(None, full_name, adminID, dob, email, password)
        new_admin.save_to_db()

        input("Press enter to return to the menu...")

    def logIn(self):
        adminCheck = input("Please enter email: ")
        if admin_email_exists(adminCheck):
            passwordAttempt = input("Please enter your password: ")
            conn = connect_db()

            if not conn:
                print("Unable to connect. Please try again later.")
                return False
            
            cursor = conn.cursor()
            cursor.execute("SELECT password, full_name FROM admins WHERE email = %s", (adminCheck,))
            result = cursor.fetchone()

            cursor.close()
            conn.close()
            if result:
                storedPassword, fullname = result

                if passwordAttempt == storedPassword:
                    print(f"Welcome, admin {fullname}!")
                    return True
                else:
                    print("Incorrect password. Access denied.")
                    return False
            else:
                print("Unexpected error: admin not found after checking existence.")
                return False
        else:
            print("No account found with that email.")
        return True




if __name__ == "__main__":
    pass