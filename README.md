# Personal Expense Tracker

A simple personal expense tracker built with Python, FastAPI, SQLAlchemy, and SQLite.

## What it does

- Add an expense
- View all expenses
- View one expense
- Update an expense
- Delete an expense
- Filter expenses by category and date range
- View total spending and spending by category
- Export expenses as a CSV file

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Pytest

## Run locally

Clone the repository and enter the project folder:

```bash
git clone https://github.com/Arun-Sanjel/personal_expense_tracker.git
cd personal_expense_tracker
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Open the API documentation at:

```
http://127.0.0.1:8000/docs
```

## Example expense

A request to add $25 of groceries:

```json
{
  "title": "Groceries",
  "amount": 25.00,
  "category": "Food",
  "expense_date": "2026-09-21",
  "notes": "Weekly groceries"
}
```

## Run tests

```bash
pytest
```

The SQLite database file is created automatically when the application starts.
