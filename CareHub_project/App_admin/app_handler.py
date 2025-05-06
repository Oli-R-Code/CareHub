from common.database import *
from .sp_handler import *
from .doc_handler import *
from .sch_handler import *
from .appointment_handler import *
from App_admin.add_availability import *
def app_handler():
    while True:
        choice = input("""Please choose an operation
A) Add or remove specialities
B) Add or remove doctors
C) Add, edit or remove doctor's schedule
D) Check appointments request
E) Log out
F) Bulk add doctor availability
""")
        match choice.upper():
            case 'A':
                sp_handler()
            case 'B':
                doc_handler()
            case 'C':
                sch_handler()
            case 'D':
                appointment_handler()
            case 'E':
                print("Logging out...")
                break
            case 'F':
                availability_handler()
            case _:
                print("Invalid option. Please try again")

if __name__ == "__main__":
    app_handler()