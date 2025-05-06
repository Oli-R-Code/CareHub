from common.database import *

def sp_handler():
    while True:
        choice = input("""\nPlease choose a speciality operation
A) List all specialities
B) Add a new speciality
C) Remove a speciality
D) Go back
""")
        match choice.upper():
            case 'A':
                specialities = get_all_specialities()
                if not specialities:
                    print("No specialities found.")
                else:
                    print("\nAvailable Specialities:")
                    for sp in specialities:
                        print(f"{sp['specialityID']}: {sp['name']}")
            case 'B':
                name = input("Enter the new speciality name: ").strip()
                if name:
                    query = "INSERT INTO specialities (name) VALUES (%s)"
                    execute_non_select(query, (name,))
                    print(f"Speciality '{name}' added successfully.")
                else:
                    print("Speciality name cannot be empty.")
            case 'C':
                specialities = get_all_specialities()
                if not specialities:
                    print("No specialities to remove.")
                else:
                    print("\nAvailable Specialities:")
                    for sp in specialities:
                        print(f"{sp['specialityID']}: {sp['name']}")
                    try:
                        sp_id = int(input("Enter the ID of the speciality to remove: "))
                        ids = [sp['specialityID'] for sp in specialities]
                        if sp_id in ids:
                            query = "DELETE FROM specialities WHERE specialityID = %s"
                            execute_non_select(query, (sp_id,))
                            print("Speciality removed successfully.")
                        else:
                            print("Invalid speciality ID.")
                    except ValueError:
                        print("Please enter a valid number.")
            case 'D':
                break
            case _:
                print("Invalid option. Please choose A, B, C, or D.")

if __name__ == "__main__":
    sp_handler()