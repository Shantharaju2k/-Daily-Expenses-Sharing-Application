# Daily Expenses Sharing Application

## Overview
The Daily Expenses Sharing Application is a Python-based tool designed to help users manage their expenses collaboratively. Users can add expenses, split them among participants, and generate balance sheets. This application includes functionalities for user management, expense tracking, and email sharing of balance sheets.

## Features
- **User Management**
  - Create and retrieve user details.
- **Expense Management**
  - Add expenses with various split methods:
    - **Equal**: Split expenses equally among all participants.
    - **Exact**: Specify the exact amount each participant owes.
    - **Percentage**: Specify the percentage each participant owes (ensures percentages add up to 100%).
- **Balance Sheet Generation**
  - Show individual expenses and overall expenses for all users.
  - Export the balance sheet as a CSV file.
  - Send the balance sheet via email.

## Requirements
- Python 3.x
- `smtplib` for sending emails
- `csv` for exporting balance sheets

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Shantharaju2k/-Daily-Expenses-Sharing-Application.git
   cd YourRepositoryName
   ```

2. Install any required packages if necessary (all standard libraries are used in this application).

3. Update the email credentials in the code:
   - Replace `your-email@gmail.com` and `your-app-password` in the code with your Gmail address and app password.

## Usage
1. Run the application:
   ```bash
   python app.py
   ```

2. Follow the on-screen prompts to:
   - Create a user.
   - Add expenses with various split methods.
   - Retrieve user expenses.
   - Retrieve overall expenses.
   - Generate and export balance sheets.
   - Send balance sheets via email.

## Code Structure
- `User`: Class representing a user with attributes for email, name, mobile number, and their expenses.
- `Expense`: Class representing an expense with attributes for date, description, amount, and participants.
- `ExpenseTracker`: Class managing users and their expenses with methods for user and expense management.
- `main()`: The main function containing the application loop and user interface.

## Example
### Creating a User
```python
tracker.create_user('john.doe@example.com', 'John Doe', '1234567890')
```

### Adding an Expense
```python
tracker.add_expense('john.doe@example.com', 'Dinner', 100, 'equal', {})
```

### Generating a Balance Sheet
```python
tracker.export_balance_sheet('balance_sheet.csv')
```

### Sending the Balance Sheet via Email
```python
tracker.send_balance_sheet('recipient@example.com', 'balance_sheet.csv')
```

## Notes
- Ensure your Gmail account settings allow sending emails from less secure apps, or use an app password if 2-Step Verification is enabled.
- Validate the total percentages when using the percentage split method to ensure they add up to 100%.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
- [Python Documentation](https://docs.python.org/3/)
- [Gmail API](https://developers.google.com/gmail/api)

## Contact
For any questions or suggestions, feel free to reach out:
- **Name**: Shantharaju
- **Email**: shanthu2k@gmail.com
