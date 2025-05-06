from App_user.auth import *
from common.database import *
from App_user.app_handler import *

def main():
    # Connect to the database first
    connect_db()
    users_auth_Obj = users_auth()

    # Initializing isLoggedIn and isAuthenticated
    isLoggedIn = False
    user_id = None  # We'll store the user ID here

    while not isLoggedIn:
        print(""" 
CareHub – Book. Meet. Heal.       
Welcome to our appointment system

Opening hours
Mon - Fri:    7:00 - 20:00
Saturday:     9:00 - 16:00
Sundays and public holidays: 10:00 - 13:00""")
        menuChoice = input(""" 
Please choose an operation
A) LogIn
B) Sign In
""")

        match menuChoice.upper():
            case 'A':
                # Log in returns user_id if successful
                user_id = users_auth_Obj.logIn()
                if user_id:  # If login is successful, set isLoggedIn to True
                    isLoggedIn = True
            case 'B':
                users_auth_Obj.sign_In()
            case _:
                print("Invalid choice. Please enter 'A' or 'B'.")

    # After successful login, pass user_id to app_handler
    if isLoggedIn:
        print("Login successful. Proceeding to the main application...")
        app_handler(user_id)

if __name__ == "__main__":
    main()
