# Expense Tracker API

A simple REST API for tracking expenses built with Python and FastAPI.

## Features

- Add new expenses
- Retrieve all expenses
- Filter expenses by category
- Get total spending (overall and by category)
- Delete expenses

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- Pytest (for testing)

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the server:
```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Running Tests

```bash
pytest tests/
```

## API Endpoints

- `POST /expenses` - Add a new expense
- `GET /expenses` - Get all expenses
- `GET /expenses/category/{category}` - Get expenses by category
- `GET /expenses/totals` - Get total spending
- `DELETE /expenses/{expense_id}` - Delete an expense

## Example Request

```json
POST /expenses
{
  "title": "Groceries",
  "amount": 50.0,
  "category": "Food",
  "date": "2026-07-31"
}
```