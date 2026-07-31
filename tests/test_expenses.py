from fastapi.testclient import TestClient
from src.main import app
import os
import json
from datetime import date

client = TestClient(app)

def setup_function():
    """Clear expenses before each test."""
    if os.path.exists("expenses.json"):
        os.remove("expenses.json")

def test_add_expense():
    """Test adding a new expense."""
    setup_function()
    response = client.post(
        "/expenses",
        json={
            "title": "Groceries",
            "amount": 50.0,
            "category": "Food",
            "date": "2026-07-31"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Groceries"
    assert data["amount"] == 50.0
    assert data["category"] == "Food"
    assert data["date"] == "2026-07-31"
    assert data["id"] == 1

def test_get_expenses():
    """Test getting all expenses."""
    setup_function()
    # Add two expenses
    client.post("/expenses", json={
        "title": "Groceries", "amount": 50.0, "category": "Food", "date": "2026-07-31"
    })
    client.post("/expenses", json={
        "title": "Gas", "amount": 40.0, "category": "Transport", "date": "2026-07-31"
    })
    
    response = client.get("/expenses")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Groceries"
    assert data[1]["title"] == "Gas"

def test_get_expenses_by_category():
    """Test getting expenses by category."""
    setup_function()
    # Add expenses
    client.post("/expenses", json={
        "title": "Groceries", "amount": 50.0, "category": "Food", "date": "2026-07-31"
    })
    client.post("/expenses", json={
        "title": "Restaurant", "amount": 30.0, "category": "Food", "date": "2026-07-31"
    })
    client.post("/expenses", json={
        "title": "Gas", "amount": 40.0, "category": "Transport", "date": "2026-07-31"
    })
    
    # Get food expenses
    response = client.get("/expenses/category/Food")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(expense["category"] == "Food" for expense in data)
    
    # Get transport expenses
    response = client.get("/expenses/category/Transport")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["category"] == "Transport"
    
    # Test non-existent category
    response = client.get("/expenses/category/Entertainment")
    assert response.status_code == 404

def test_get_totals():
    """Test getting totals."""
    setup_function()
    # Add expenses
    client.post("/expenses", json={
        "title": "Groceries", "amount": 50.0, "category": "Food", "date": "2026-07-31"
    })
    client.post("/expenses", json={
        "title": "Restaurant", "amount": 30.0, "category": "Food", "date": "2026-07-31"
    })
    client.post("/expenses", json={
        "title": "Gas", "amount": 40.0, "category": "Transport", "date": "2026-07-31"
    })
    
    response = client.get("/expenses/totals")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 120.0
    assert data["by_category"]["Food"] == 80.0
    assert data["by_category"]["Transport"] == 40.0

def test_delete_expense():
    """Test deleting an expense."""
    setup_function()
    # Add an expense
    response = client.post("/expenses", json={
        "title": "Groceries", "amount": 50.0, "category": "Food", "date": "2026-07-31"
    })
    expense_id = response.json()["id"]
    
    # Delete it
    response = client.delete(f"/expenses/{expense_id}")
    assert response.status_code == 204
    
    # Verify it's gone
    response = client.get("/expenses")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0
    
    # Try to delete non-existent expense
    response = client.delete("/expenses/999")
    assert response.status_code == 404

def test_validation():
    """Test that FastAPI validates input."""
    setup_function()
    # Missing required field
    response = client.post("/expenses", json={
        "title": "Groceries",
        "amount": 50.0,
        # missing category
        "date": "2026-07-31"
    })
    assert response.status_code == 422
    
    # Wrong type
    response = client.post("/expenses", json={
        "title": "Groceries",
        "amount": "fifty",  # should be float
        "category": "Food",
        "date": "2026-07-31"
    })
    assert response.status_code == 422