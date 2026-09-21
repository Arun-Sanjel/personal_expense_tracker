from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class ExpenseBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    amount: float = Field(gt=0)
    category: str = Field(min_length=1, max_length=50)
    expense_date: date
    notes: str | None = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    amount: float | None = Field(default=None, gt=0)
    category: str | None = Field(default=None, min_length=1, max_length=50)
    expense_date: date | None = None
    notes: str | None = None


class ExpenseResponse(ExpenseBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CategoryTotal(BaseModel):
    category: str
    total: float


class ExpenseSummary(BaseModel):
    total_spending: float
    number_of_expenses: int
    by_category: list[CategoryTotal]
