from datetime import date

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_and_get_expense():
    response = client.post(
        "/expenses",
        json={
            "title": "Groceries",
            "amount": 25.00,
            "category": "Food",
            "expense_date": str(date.today()),
            "notes": "Weekly groceries",
        },
    )

    assert response.status_code == 201
    expense_id = response.json()["id"]

    get_response = client.get(f"/expenses/{expense_id}")

    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Groceries"
    assert get_response.json()["amount"] == 25.0


def test_invalid_amount_is_rejected():
    response = client.post(
        "/expenses",
        json={
            "title": "Invalid expense",
            "amount": -10,
            "category": "Other",
            "expense_date": str(date.today()),
        },
    )

    assert response.status_code == 422
