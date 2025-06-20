import json
import os

# --- File Paths ---
PATIENT_FILE = "/storage/emulated/0/PyProjects/patients.json"
APPOINT_FILE = "/storage/emulated/0/PyProjects/appointments.json"

# --- Load Functions ---
def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return []

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# --- Core Data ---
patients = load_data(PATIENT_FILE)
appointments = load_data(APPOINT_FILE)

# --- Patient Features ---
def add_patient():
    patient = {
        "id": input("Enter Patient ID: "),
        "name": input("Enter Name: "),
        "age": input("Enter Age: "),
        "gender": input("Enter Gender: "),
        "diagnosis": input("Enter Diagnosis: ")
    }
    patients.append(patient)
    save_data(PATIENT_FILE, patients)
    print("✅ Patient added.\n")

def view_patients():
    if not patients:
        print("❌ No patients found.\n")
        return
    print("\n--- All Patients ---")
    for p in patients:
        print(f"{p['id']} | {p['name']} | {p['age']} | {p['gender']} | {p['diagnosis']}")
    print()

def search_patient():
    pid = input("Enter Patient ID: ")
    for p in patients:
        if p["id"] == pid:
            print(f"✅ Found: {p['name']} ({p['age']} - {p['gender']}) - Diagnosis: {p['diagnosis']}\n")
            return
    print("❌ Not found.\n")

def delete_patient():
    pid = input("Enter Patient ID to delete: ")
    for p in patients:
        if p["id"] == pid:
            patients.remove(p)
            save_data(PATIENT_FILE, patients)
            print("🗑️ Patient deleted.\n")
            return
    print("❌ Not found.\n")

# --- Appointment Features ---
def book_appointment():
    pid = input("Enter Patient ID: ")
    if not any(p["id"] == pid for p in patients):
        print("❌ Patient not found.\n")
        return
    date = input("Enter Appointment Date (YYYY-MM-DD): ")
    reason = input("Reason for Appointment: ")
    appointment = {"patient_id": pid, "date": date, "reason": reason}
    appointments.append(appointment)
    save_data(APPOINT_FILE, appointments)
    print("📅 Appointment booked.\n")

def view_appointments():
    if not appointments:
        print("❌ No appointments yet.\n")
        return
    print("\n--- Appointments ---")
    for a in appointments:
        print(f"Patient ID: {a['patient_id']} | Date: {a['date']} | Reason: {a['reason']}")
    print()

# --- Main Menu ---
def menu():
    while True:
        print("\n🏥 Hospital Management System")
        print("1. Add Patient")
        print("2. View All Patients")
        print("3. Search Patient by ID")
        print("4. Delete Patient")
        print("5. Book Appointment")
        print("6. View Appointments")
        print("7. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            add_patient()
        elif choice == "2":
            view_patients()
        elif choice == "3":
            search_patient()
        elif choice == "4":
            delete_patient()
        elif choice == "5":
            book_appointment()
        elif choice == "6":
            view_appointments()
        elif choice == "7":
            break
        else:
            print("❌ Invalid option.\n")

# --- Run ---
menu()