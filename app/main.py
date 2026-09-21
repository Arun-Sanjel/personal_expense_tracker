import csv
import io

from datetime import date

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from . import crud
from .database import Base, engine, get_db
from .schemas import (
    ExpenseCreate,
    ExpenseResponse,
    ExpenseSummary,
    ExpenseUpdate,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Personal Expense Tracker",
    description="A simple API for recording and reviewing personal expenses.",
    version="1.0.0",
)


@app.get("/")
def read_root():
    return {"message": "Personal Expense Tracker API is running"}


@app.post("/expenses", response_model=ExpenseResponse, status_code=201)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    return crud.create_expense(db, expense)


@app.get("/expenses", response_model=list[ExpenseResponse])
def list_expenses(
    category: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date cannot be after end_date",
        )

    return crud.get_expenses(db, category, start_date, end_date)


@app.get("/expenses/summary", response_model=ExpenseSummary)
def expense_summary(db: Session = Depends(get_db)):
    return crud.get_summary(db)


@app.get("/expenses/export")
def export_expenses(db: Session = Depends(get_db)):
    expenses = crud.get_expenses(db)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        ["id", "title", "amount", "category", "expense_date", "notes"]
    )

    for expense in expenses:
        writer.writerow(
            [
                expense.id,
                expense.title,
                expense.amount,
                expense.category,
                expense.expense_date,
                expense.notes or "",
            ]
        )

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=expenses.csv"
        },
    )


@app.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def get_one_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = crud.get_expense(db, expense_id)

    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    return expense


@app.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_one_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    db: Session = Depends(get_db),
):
    expense = crud.get_expense(db, expense_id)

    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    return crud.update_expense(db, expense, expense_data)


@app.delete("/expenses/{expense_id}")
def delete_one_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = crud.get_expense(db, expense_id)

    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    crud.delete_expense(db, expense)
    return {"message": "Expense deleted successfully"}
