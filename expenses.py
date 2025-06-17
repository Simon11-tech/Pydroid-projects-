import os
from datetime import datetime

FILE_NAME = "finance_data.txt"

def add_transaction():
    amount = float(input("Enter amount: "))
    trans_type = input("Type (income/expense): ").lower()
    category = input("Category (e.g. food, transport): ")
    note = input("Note (optional): ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M")

    if trans_type not in ["income", "expense"]:
        print("❌ Invalid transaction type.")
        return

    with open(FILE_NAME, "a") as file:
        file.write(f"{date},{trans_type},{amount},{category},{note}\n")
    
    print("✅ Transaction recorded.")

def view_balance():
    income = 0
    expense = 0

    if not os.path.exists(FILE_NAME):
        print("No transactions yet.")
        return

    with open(FILE_NAME, "r") as file:
        for line in file:
            _, trans_type, amount, *_ = line.strip().split(",")
            amount = float(amount)
            if trans_type == "income":
                income += amount
            else:
                expense += amount
    
    print(f"\n💰 Total Income: ₦{income}")
    print(f"💸 Total Expenses: ₦{expense}")
    print(f"📊 Balance: ₦{income - expense}")

def view_history():
    if not os.path.exists(FILE_NAME):
        print("No transactions yet.")
        return

    print("\n📜 Transaction History:")
    with open(FILE_NAME, "r") as file:
        for line in file:
            date, t_type, amount, cat, note = line.strip().split(",")
            print(f"{date} | {t_type.title()} | ₦{amount} | {cat} | {note}")

def main():
    while True:
        print("\n=== Personal Finance Tracker ===")
        print("1. Add Transaction")
        print("2. View Balance")
        print("3. View History")
        print("4. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_balance()
        elif choice == "3":
            view_history()
        elif choice == "4":
            print("👋 Exiting... Stay rich!")
            break
        else:
            print("❌ Invalid choice.")

main()