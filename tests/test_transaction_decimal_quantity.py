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


def test_transaction_decimal_quantity():
    """Test that transactions support decimal quantities."""
    user_id = get_user_id()
    
    # Test creating transaction with decimal quantity and datetime
    payload = {
        "title": "Decimal Quantity Test",
        "description": "Testing decimal quantity support",
        "owner_id": user_id,
        "transaction_type": "expense",
        "amount_per_unit": "100.00",
        "quantity": 2.5,
        "date": "2025-11-07T10:30:00"
    }
    r = client.post("/transactions", json=payload)
    assert r.status_code == 201, r.text
    created = r.json()
    
    # Verify decimal quantity is preserved
    assert Decimal(created["quantity"]) == Decimal("2.5")
    assert created["amount_per_unit"] == "100.00"
    
    # Verify total_amount calculation with decimal
    expected_total = Decimal("100.00") * Decimal("2.5")
    assert Decimal(created["total_amount"]) == expected_total
    assert created["total_amount"] == "250.00"
    
    transaction_id = created["id"]
    
    # Test updating with different decimal quantity
    update_payload = {
        "quantity": 3.75
    }
    r_update = client.put(f"/transactions/{transaction_id}", json=update_payload)
    assert r_update.status_code == 200, r_update.text
    updated = r_update.json()
    
    assert Decimal(updated["quantity"]) == Decimal("3.75")
    expected_total_updated = Decimal("100.00") * Decimal("3.75")
    assert Decimal(updated["total_amount"]) == expected_total_updated
    assert updated["total_amount"] == "375.00"


def test_transaction_integer_quantity_still_works():
    """Test that integer quantities still work (backward compatibility)."""
    user_id = get_user_id()
    
    payload = {
        "title": "Integer Quantity Test",
        "owner_id": user_id,
        "transaction_type": "earning",
        "amount_per_unit": "50.00",
        "quantity": 10,  # Integer
        "date": "2025-11-07T09:00:00"
    }
    r = client.post("/transactions", json=payload)
    assert r.status_code == 201, r.text
    created = r.json()
    
    # Integer should be converted to decimal
    assert Decimal(created["quantity"]) == Decimal("10.0")
    assert Decimal(created["total_amount"]) == Decimal("500.00")


def test_transaction_fractional_quantities():
    """Test various fractional quantity values."""
    user_id = get_user_id()
    
    test_cases = [
        ("0.5", Decimal("0.5")),
        ("1.333", Decimal("1.333")),
        ("99.999", Decimal("99.999")),
        (0.25, Decimal("0.25")),
        (1.5, Decimal("1.5")),
    ]
    
    for quantity_input, expected_quantity in test_cases:
        payload = {
            "title": f"Fractional Test {quantity_input}",
            "owner_id": user_id,
            "transaction_type": "expense",
            "amount_per_unit": "10.00",
            "quantity": quantity_input,
            "date": "2025-11-07T15:45:00"
        }
        r = client.post("/transactions", json=payload)
        assert r.status_code == 201, r.text
        created = r.json()
        
        # Check quantity with tolerance for rounding
        assert abs(Decimal(created["quantity"]) - expected_quantity) < Decimal("0.001")
        
        # Verify total amount calculation
        expected_total = Decimal("10.00") * expected_quantity
        assert abs(Decimal(created["total_amount"]) - expected_total) < Decimal("0.01")


def test_transaction_quantity_precision():
    """Test that quantity precision is maintained up to 3 decimal places."""
    user_id = get_user_id()
    
    payload = {
        "title": "Precision Test",
        "owner_id": user_id,
        "transaction_type": "expense",
        "amount_per_unit": "7.50",
        "quantity": 2.125,  # Exact 3 decimal places
        "date": "2025-11-07T18:20:00"
    }
    r = client.post("/transactions", json=payload)
    assert r.status_code == 201, r.text
    created = r.json()
    
    assert created["quantity"] == "2.125"
    expected_total = Decimal("7.50") * Decimal("2.125")
    assert Decimal(created["total_amount"]) == expected_total.quantize(Decimal("0.01"))
