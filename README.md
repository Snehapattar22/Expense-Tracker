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


## Screenshots
<img width="1857" height="947" alt="Screenshot 2025-12-04 155109" src="https://github.com/user-attachments/assets/974741b9-779a-4bf0-a9d7-2b022c43a692" />
<img width="1844" height="1024" alt="Screenshot 2025-12-04 155130" src="https://github.com/user-attachments/assets/faccd80a-a972-4d71-a093-7517d7e34219" />
<img width="1861" height="1010" alt="Screenshot 2025-12-04 155209" src="https://github.com/user-attachments/assets/c1432059-f8c2-4ff4-8710-8ad13d00406d" />
<img width="1860" height="981" alt="Screenshot 2025-12-04 155227" src="https://github.com/user-attachments/assets/5a4cdc3e-d2f5-4f21-a36a-ee3cfc696455" />
