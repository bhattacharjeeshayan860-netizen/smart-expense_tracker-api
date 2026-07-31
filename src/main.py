from fastapi import FastAPI, HTTPException
from src.models import Expense, ExpenseCreate
from src.storage import (
    create_expense,
    get_expenses,
    get_expense_by_id,
    get_expenses_by_category,
    update_expense,
    delete_expense,
)
from typing import List, Dict

app = FastAPI(title="Expense Tracker API")


@app.post("/expenses", status_code=201)
def add_expense(expense: ExpenseCreate):
    """Add a new expense."""
    return create_expense(expense)


@app.get("/expenses", response_model=List[Expense])
def list_expenses():
    """Get all expenses."""
    return get_expenses()


@app.get("/expenses/category/{category}", response_model=List[Expense])
def get_expenses_by_category_endpoint(category: str):
    """Get expenses filtered by category."""
    expenses = get_expenses_by_category(category)
    if not expenses:
        raise HTTPException(status_code=404, detail=f"No expenses found for category: {category}")
    return expenses


@app.get("/expenses/totals")
def get_totals():
    """Get total amount overall and per category."""
    expenses = get_expenses()
    total = sum(expense.amount for expense in expenses)
    by_category: Dict[str, float] = {}
    for expense in expenses:
        by_category[expense.category] = by_category.get(expense.category, 0) + expense.amount
    return {"total": total, "by_category": by_category}


@app.delete("/expenses/{expense_id}", status_code=204)
def delete_expense_endpoint(expense_id: int):
    """Delete an expense by ID."""
    success = delete_expense(expense_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Expense with ID {expense_id} not found")
    return None  # 204 No Content