from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .models import Expense
from .schemas import ExpenseCreate, ExpenseUpdate


def create_expense(db: Session, expense_data: ExpenseCreate) -> Expense:
    expense = Expense(**expense_data.model_dump())
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def get_expenses(
    db: Session,
    category: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[Expense]:
    statement = select(Expense).order_by(Expense.expense_date.desc())

    if category:
        statement = statement.where(Expense.category == category)

    if start_date:
        statement = statement.where(Expense.expense_date >= start_date)

    if end_date:
        statement = statement.where(Expense.expense_date <= end_date)

    return list(db.scalars(statement).all())


def get_expense(db: Session, expense_id: int) -> Expense | None:
    return db.get(Expense, expense_id)


def update_expense(
    db: Session,
    expense: Expense,
    expense_data: ExpenseUpdate,
) -> Expense:
    changes = expense_data.model_dump(exclude_unset=True)

    for field, value in changes.items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)
    return expense


def delete_expense(db: Session, expense: Expense) -> None:
    db.delete(expense)
    db.commit()


def get_summary(db: Session) -> dict:
    total = db.scalar(select(func.coalesce(func.sum(Expense.amount), 0.0)))
    count = db.scalar(select(func.count(Expense.id)))

    category_rows = db.execute(
        select(Expense.category, func.sum(Expense.amount))
        .group_by(Expense.category)
        .order_by(func.sum(Expense.amount).desc())
    ).all()

    return {
        "total_spending": round(float(total or 0), 2),
        "number_of_expenses": int(count or 0),
        "by_category": [
            {"category": category, "total": round(float(total), 2)}
            for category, total in category_rows
        ],
    }
