from common.database import get_all_specialities, get_doctors_by_speciality
from appointments import *

def app_handler():
    while True:
        print("\nPlease select from the following menu:\n")

        specialities = get_all_specialities()
        if not specialities:
            print("No specialities found in the system.")
            return

        description_map = {
            "A": """General Practitioner
If this is your first appointment with us, we recommend starting here! The General Practitioner (GP) is your first point of contact for most medical concerns. They can refer you to specialists if needed.""",

            "B": """Cardiology
For issues related to your heart or blood vessels. Cardiologists specialize in diagnosing and treating heart conditions.""",

            "C": """Gynecology
For reproductive and menstrual health, pregnancy care, and related concerns.""",

            "D": """Pediatrics
For children's health, from infancy through adolescence. Pediatricians specialize in the care and treatment of young patients."""
        }

        letter_keys = list(description_map.keys())

        for i, spec in enumerate(specialities):
            if i < len(letter_keys):
                key = letter_keys[i]
                print(f"{key}) {description_map[key]}\n")
            else:
                print(f"{i+1}) {spec['name']}\n   {spec['description']}\n")

        print("F) Log out")

        choice = input("\nEnter your choice: ").strip().upper()

        if choice == 'F':
            print("Logging out...")
            return False

        if choice in letter_keys:
            index = letter_keys.index(choice)
        elif choice.isdigit():
            index = int(choice) - 1
        else:
            index = -1

        if 0 <= index < len(specialities):
            selected = specialities[index]
            specialityID = selected['specialityID']
            print(f"\nYou selected: {selected['name']}")

            doctors = get_doctors_by_speciality(specialityID)
            if doctors:
                print("\nAvailable doctors:")
                for i, doc in enumerate(doctors, start=1):
                    print(f"{i}) Dr. {doc['full_name']} (Hours: {doc['working_hours']})")

                doctor_choice = input("\nSelect a doctor by number or enter 'F' to go back: ").strip().upper()

                if doctor_choice == 'F':
                    continue

                if doctor_choice.isdigit():
                    doctor_index = int(doctor_choice) - 1
                    if 0 <= doctor_index < len(doctors):
                        selected_doctor = doctors[doctor_index]
                        print(f"\nYou selected: Dr. {selected_doctor['full_name']}")

                        # Call the function with the correct doctor ID
                        show_available_slots(selected_doctor['doctorID'])
                        
                    else:
                        print("Invalid doctor choice. Please try again.")
                else:
                    print("Invalid input. Please enter a number corresponding to a doctor.")
            else:
                print("No doctors available for this speciality.")
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    from common.database import connect_db
    connect_db()
    app_handler()
