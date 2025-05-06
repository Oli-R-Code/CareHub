from common.database import *
from App_admin.auth import *
from App_admin.app_handler import *

def main():
    #to connect to database first
    connect_db()

    #initializing isloggedin first as false
    isLoggedIn = False
    isAuthenticated = False
    authObj = admin_auth()

    while not isAuthenticated:
        print("""
CareHub – Book. Meet. Heal.       
Welcome to our admin system""")
        
        menuChoice = input("""
Please choose an operation
A) LogIn
B) Sign In
""")

        match menuChoice.upper():
                case 'A':
                    #because logIn returns isLoggedIn true when autenticates
                    isLoggedIn = authObj.logIn()
                case 'B':
                    authObj.sign_In()
                case _:
                    print("Invalid choice. Please enter 'A' or 'B'.")

        while isLoggedIn:
            isLoggedIn = app_handler()

        if not isLoggedIn:
                print("Returning to the main menu...")


if __name__ == "__main__":
    main()