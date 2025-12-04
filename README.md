# Expense Tracker

## About the Project:
This application allows users to record their daily expenses, organize them into categories, set monthly budgets for each category, and view spending reports. The system provides notifications if the spending exceeds the assigned budget and also supports month-specific budgets. The interface is very simple and user-friendly, permitting fast tracking and monitoring of expenses.

## Features Implemented:

- Add daily expenses with category, amount, date, and notes
- Categorized expenses (Food, Transport, Entertainment, Groceries, Utilities, etc.)
- Set monthly budgets for each category
- Set different budgets for different months (YYYY-MM format)
- Alert when a budget is exceeded
- Alert when 90% of a budget is used
- Monthly total spending report
- Category wise spending vs budget comparison

## Tech Stack Used:

- Python
- SQLite
- SQLAlchemy ORM
- HTML, CSS, Jinja2
- Docker
- Pytest

## How to Run the Project Locally:

### Create Virtual Environment
#### Windows:
- python -m venv venv
- venv\Scripts\activate

#### Mac/Linux:
- python3 -m venv venv
- source venv/bin/activate

### Install Dependencies
- pip install -r requirements.txt

### Initialize the Database
- python db_init.py

### Start the Application
- python app.py

### Open in browser:
- http://localhost:5000

## How to Run the Project Using Docker:

### Build Docker Image
- docker build -t expense-tracker .

### Run Docker Container
- docker run -p 5000:5000 expense-tracker

### Open in browser:
- http://localhost:5000

## Edge Cases Handled

- Validates positive amount for every expense
- Ensures required fields (amount/category) are not empty
- Handles invalid date input formats safely
- Prevents duplicate month budgets (updates instead of inserting)
- Supports very large expense values without crashing
- Monthly budget overrides general budget correctly
- App continues working if email alert settings are not configured
- Shows proper messages when no expenses exist
- Shared-group field is optional and stored safely
- Database auto creates if missing
