from datetime import datetime
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class User:
    def __init__(self, email, name, mobile):
        self.email = email
        self.name = name
        self.mobile = mobile
        self.expenses = []


class Expense:
    def __init__(self, date, description, amount, participants):
        self.date = date
        self.description = description
        self.amount = amount
        self.participants = participants  # List of participants


class ExpenseTracker:
    def __init__(self):
        self.users = []

    def create_user(self, email, name, mobile):
        user = User(email, name, mobile)
        self.users.append(user)
        return "User added successfully."

    def get_user(self, email):
        for user in self.users:
            if user.email == email:
                return user
        return None

    def add_expense(self, email, description, amount, split_method, split_details):
        user = self.get_user(email)
        if user:
            date = datetime.now().strftime("%d-%m-%Y")
            if split_method == "equal":
                participants = [p for p in self.users]
                split_amount = amount / len(participants)
                expense = Expense(date, description, amount, participants)
                for participant in participants:
                    participant.expenses.append((expense, split_amount))
            elif split_method == "exact":
                participants = split_details.keys()
                expense = Expense(date, description, amount, participants)
                for participant in participants:
                    split_amount = split_details[participant]
                    participant.expenses.append((expense, split_amount))
            elif split_method == "percentage":
                participants = split_details.keys()
                total_percentage = sum(split_details.values())
                if total_percentage != 100:
                    raise ValueError("Percentages must add up to 100.")
                expense = Expense(date, description, amount, participants)
                for participant in participants:
                    split_amount = (split_details[participant] / 100) * amount
                    participant.expenses.append((expense, split_amount))
            return "Expense added successfully."
        return "User not found."

    def get_user_expenses(self, email):
        user = self.get_user(email)
        if user:
            return user.expenses
        return []

    def get_overall_expenses(self):
        all_expenses = []
        for user in self.users:
            all_expenses.extend(user.expenses)
        return all_expenses

    def generate_balance_sheet(self):
        balance_sheet = []
        for user in self.users:
            total_expenses = sum(amount for expense, amount in user.expenses)
            balance_sheet.append(f"{user.name} ({user.email}): Total Expenses: ${total_expenses:.2f}")
        return balance_sheet

    def export_balance_sheet(self, file_name='balance_sheet.csv'):
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['User Name', 'User Email', 'Total Expenses'])
            for user in self.users:
                total_expenses = sum(amount for expense, amount in user.expenses)
                writer.writerow([user.name, user.email, total_expenses])
        return f"Balance sheet exported as {file_name}."

    def send_balance_sheet(self, recipient_email, file_name='balance_sheet.csv'):
        sender_email = "your-email@gmail.com"  # Replace with your email
        sender_password = "your-app-password"  # Use your app password here

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "Your Balance Sheet"

        body = "Please find attached the balance sheet for your expenses."
        msg.attach(MIMEText(body, 'plain'))

        with open(file_name, 'r') as f:
            attachment = MIMEText(f.read(), _subtype='csv')
            attachment.add_header('Content-Disposition', 'attachment', filename=file_name)
            msg.attach(attachment)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)  # Use app password here
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)
            server.quit()
            return f"Balance sheet sent to {recipient_email}."
        except Exception as e:
            return f"Failed to send email: {e}"


def validate_percentage_sums(split_details):
    total = sum(split_details.values())
    if total != 100:
        raise ValueError("Percentages must add up to 100.")


def main():
    tracker = ExpenseTracker()

    while True:
        print("\nExpense Tracker Menu:")
        print("1. Create User")
        print("2. Add Expense")
        print("3. Retrieve User Expenses")
        print("4. Retrieve Overall Expenses")
        print("5. Generate Balance Sheet")
        print("6. Export Balance Sheet")
        print("7. Send Balance Sheet via Email")
        print("8. Exit")

        try:
            choice = input("Enter your choice (1-8): ")

            if choice == "1":
                email = input("Enter user's email: ")
                name = input("Enter user's name: ")
                mobile = input("Enter user's mobile number: ")
                print(tracker.create_user(email, name, mobile))

            elif choice == "2":
                email = input("Enter the user's email to add expense: ")
                description = input("Enter expense description: ")
                amount = float(input("Enter the expense amount: "))
                split_method = input("Enter split method (equal, exact, percentage): ")

                if split_method == "exact":
                    split_details = {}
                    while True:
                        participant_email = input("Enter participant's email (or 'done' to finish): ")
                        if participant_email.lower() == 'done':
                            break
                        split_amount = float(input(f"Enter exact amount for {participant_email}: "))
                        split_details[tracker.get_user(participant_email)] = split_amount
                    tracker.add_expense(email, description, amount, split_method, split_details)

                elif split_method == "percentage":
                    split_details = {}
                    while True:
                        participant_email = input("Enter participant's email (or 'done' to finish): ")
                        if participant_email.lower() == 'done':
                            break
                        percentage = float(input(f"Enter percentage for {participant_email}: "))
                        split_details[tracker.get_user(participant_email)] = percentage
                    validate_percentage_sums(split_details)
                    tracker.add_expense(email, description, amount, split_method, split_details)

                else:
                    tracker.add_expense(email, description, amount, split_method, {})

            elif choice == "3":
                email = input("Enter the user's email to retrieve expenses: ")
                user_expenses = tracker.get_user_expenses(email)
                if user_expenses:
                    for expense, amount in user_expenses:
                        print(f"{expense.date} - {expense.description}: ${amount:.2f}")
                else:
                    print("No expenses found for this user.")

            elif choice == "4":
                expenses = tracker.get_overall_expenses()
                for expense, amount in expenses:
                    print(f"{expense.date} - {expense.description}: ${amount:.2f}")

            elif choice == "5":
                balance_sheet = tracker.generate_balance_sheet()
                for line in balance_sheet:
                    print(line)

            elif choice == "6":
                file_name = input("Enter file name for the CSV (default: 'balance_sheet.csv'): ") or 'balance_sheet.csv'
                print(tracker.export_balance_sheet(file_name))

            elif choice == "7":
                recipient_email = input("Enter the recipient's email: ")
                file_name = input("Enter file name of the CSV to send (default: 'balance_sheet.csv'): ") or 'balance_sheet.csv'
                print(tracker.send_balance_sheet(recipient_email, file_name))

            elif choice == "8":
                print("Exiting the program.")
                break

            else:
                print("Invalid choice. Please enter a valid option (1-8).")

        except ValueError as e:
            print(e)

if __name__ == "__main__":
    main()
