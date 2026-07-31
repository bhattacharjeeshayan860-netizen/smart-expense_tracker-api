import json
import os
from typing import List, Optional
from src.models import Expense, ExpenseCreate
from datetime import date

DATA_FILE = "expenses.json"

def load_expenses() -> List[Expense]:
    """Load expenses from JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    expenses = []
    for item in data:
        # Convert date string back to date object
        item['date'] = date.fromisoformat(item['date'])
        expenses.append(Expense(**item))
    
    return expenses

def save_expenses(expenses: List[Expense]) -> None:
    """Save expenses to JSON file."""
    data = []
    for expense in expenses:
        expense_dict = expense.dict()
        # Convert date object to ISO format string for JSON serialization
        expense_dict['date'] = expense_dict['date'].isoformat()
        data.append(expense_dict)
    
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_next_id(expenses: List[Expense]) -> int:
    """Get the next available ID."""
    if not expenses:
        return 1
    return max(expense.id for expense in expenses) + 1

def create_expense(expense_create: ExpenseCreate) -> Expense:
    """Create a new expense."""
    expenses = load_expenses()
    expense_id = get_next_id(expenses)
    expense = Expense(id=expense_id, **expense_create.dict())
    expenses.append(expense)
    save_expenses(expenses)
    return expense

def get_expenses() -> List[Expense]:
    """Get all expenses."""
    return load_expenses()

def get_expense_by_id(expense_id: int) -> Optional[Expense]:
    """Get expense by ID."""
    expenses = load_expenses()
    for expense in expenses:
        if expense.id == expense_id:
            return expense
    return None

def get_expenses_by_category(category: str) -> List[Expense]:
    """Get expenses by category."""
    expenses = load_expenses()
    return [expense for expense in expenses if expense.category.lower() == category.lower()]

def update_expense(expense_id: int, expense_update: ExpenseCreate) -> Optional[Expense]:
    """Update an existing expense."""
    expenses = load_expenses()
    for i, expense in enumerate(expenses):
        if expense.id == expense_id:
            expense = Expense(id=expense_id, **expense_update.dict())
            expenses[i] = expense
            save_expenses(expenses)
            return expense
    return None

def delete_expense(expense_id: int) -> bool:
    """Delete an expense by ID."""
    expenses = load_expenses()
    for i, expense in enumerate(expenses):
        if expense.id == expense_id:
            del expenses[i]
            save_expenses(expenses)
            return True
    return False