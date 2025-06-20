import json
import os
import datetime

# --- File paths ---
DATA_FILE = "/storage/emulated/0/PyProjects/students.json"
BACKUP_FOLDER = "/storage/emulated/0/PyProjects/backups/"
USERNAME = "admin"
PASSWORD = "1234"

# --- Load student data ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

# --- Save student data ---
def save_data(students):
    with open(DATA_FILE, "w") as file:
        json.dump(students, file, indent=4)

# --- Backup student data with timestamp ---
def backup_data(students):
    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"students_backup_{timestamp}.json"
    path = os.path.join(BACKUP_FOLDER, filename)
    with open(path, "w") as file:
        json.dump(students, file, indent=4)
    print(f"✅ Backup saved to: {path}\n")

# --- Add a new student ---
def add_student():
    student = {
        "id": input("Enter Student ID: "),
        "name": input("Enter Student Name: "),
        "level": input("Enter Level (e.g., 100, 200): "),
        "department": input("Enter Department: ")
    }
    students.append(student)
    save_data(students)
    print("✅ Student added.\n")

# --- View all students ---
def view_students():
    if not students:
        print("❌ No students found.\n")
        return
    print("\n--- All Students ---")
    for s in students:
        print(f"{s['id']} | {s['name']} | {s['level']} | {s['department']}")
    print()

# --- Search by ID ---
def search_student():
    sid = input("Enter Student ID: ")
    for s in students:
        if s["id"] == sid:
            print(f"✅ Found: {s['name']} ({s['level']} - {s['department']})\n")
            return
    print("❌ Not found.\n")

# --- Delete by ID ---
def delete_student():
    sid = input("Enter Student ID to delete: ")
    for s in students:
        if s["id"] == sid:
            students.remove(s)
            save_data(students)
            print("🗑️ Student deleted.\n")
            return
    print("❌ Not found.\n")

# --- Login system ---
def login():
    print("🔐 Login Required")
    user = input("Username: ")
    pw = input("Password: ")
    if user == USERNAME and pw == PASSWORD:
        print("✅ Login successful.\n")
        return True
    else:
        print("❌ Access Denied.\n")
        return False

# --- Menu system ---
def menu():
    while True:
        print("📘 School Management System")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student by ID")
        print("4. Delete Student")
        print("5. Backup Data")
        print("6. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            backup_data(students)
        elif choice == "6":
            break
        else:
            print("❌ Invalid option. Try again.\n")

# --- Run app ---
if login():
    students = load_data()
    menu()
else:
    print("🔒 Exiting app.")