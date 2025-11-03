import pytest
from fastapi.testclient import TestClient
from decimal import Decimal
from main import app, seed, SessionLocal, Base, engine
from sqlalchemy import select
from app.models.user import User

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()
    yield


def get_user_id():
    db = SessionLocal()
    try:
        user = db.scalars(select(User)).first()
        return user.id
    finally:
        db.close()


def test_create_and_filter_transaction():
    user_id = get_user_id()
    # Create transaction
    payload = {
        "title": "Filter Test",
        "description": "Testing filters",
        "owner_id": user_id,
        "transaction_type": "expense",
        "amount_per_unit": "321.50",
        "quantity": 2,
        "date": "2025-10-24"
    }
    r = client.post("/transactions", json=payload)
    assert r.status_code == 201, r.text
    created = r.json()
    assert created["amount_per_unit"] == "321.50"
    assert created["quantity"] == 2
    assert created["total_amount"] == str(Decimal("321.50") * 2)

    # Filter by owner
    r_owner = client.get(f"/transactions/search?owner_id={user_id}")
    assert r_owner.status_code == 200
    assert any(t["id"] == created["id"] for t in r_owner.json())

    # Filter by transaction type
    r_type = client.get("/transactions/search?transaction_type=expense")
    assert r_type.status_code == 200
    assert any(t["id"] == created["id"] for t in r_type.json())
