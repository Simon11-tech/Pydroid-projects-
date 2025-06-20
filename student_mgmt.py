import json
import os

DATA_FILE = "/storage/emulated/0/PyProjects/students.json"

# Load student data from file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

# Save student data to file
def save_data(students):
    with open(DATA_FILE, "w") as file:
        json.dump(students, file, indent=4)

# Add a new student
def add_student():
    student = {
        "id": input("Enter Student ID: "),
        "name": input("Enter Student Name: "),
        "level": input("Enter Level (e.g., 100, 200): "),
        "department": input("Enter Department: ")
    }
    students.append(student)
    save_data(students)
    print("✅ Student added successfully.\n")

# View all students
def view_students():
    if not students:
        print("❌ No students found.\n")
        return
    print("\n--- All Students ---")
    for s in students:
        print(f"{s['id']} | {s['name']} | {s['level']} | {s['department']}")
    print()

# Search student by ID
def search_student():
    sid = input("Enter Student ID to search: ")
    for s in students:
        if s["id"] == sid:
            print(f"✅ Found: {s['name']} ({s['level']} - {s['department']})\n")
            return
    print("❌ Student not found.\n")

# Delete student by ID
def delete_student():
    sid = input("Enter Student ID to delete: ")
    for s in students:
        if s["id"] == sid:
            students.remove(s)
            save_data(students)
            print("🗑️ Student deleted.\n")
            return
    print("❌ Student not found.\n")

# Menu
def menu():
    while True:
        print("📘 School Management System")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student by ID")
        print("4. Delete Student")
        print("5. Exit")
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
            break
        else:
            print("❌ Invalid option. Try again.\n")

# Run the app
students = load_data()
menu()