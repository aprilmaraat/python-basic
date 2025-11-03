import pytest
from fastapi.testclient import TestClient
from decimal import Decimal
from main import app, seed, SessionLocal, Base, engine
from sqlalchemy import select
from app.models.category import Category
from app.models.weight import Weight

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

def get_refs():
    db = SessionLocal()
    try:
        cat = db.scalars(select(Category).where(Category.name=="LPG")).first()
        wt = db.scalars(select(Weight).where(Weight.name=="11kg")).first()
        return cat.id, wt.id
    finally:
        db.close()

def test_inventory_decimal_prices_round_trip():
    cat_id, wt_id = get_refs()
    payload = {
        "name": "Decimal Item",
        "shortname": "DI",
        "purchase_price": "12.345",
        "selling_price": 45.6789,
        "quantity": 10,
        "category_id": cat_id,
        "weight_id": wt_id
    }
    r = client.post("/inventory", json=payload)
    assert r.status_code == 201, r.text
    created = r.json()
    # Expect two decimal places rounding
    assert created["selling_price"] == str(Decimal("45.6789").quantize(Decimal("0.01")))
    assert created["selling_price"].endswith(".68")
    assert created["selling_price"] == "45.68"
    assert created["purchase_price"] == "12.35"

    inv_id = created["id"]
    # Update purchase_price and selling_price
    upd = client.put(f"/inventory/{inv_id}", json={"purchase_price": 99, "selling_price": "100.1"})
    assert upd.status_code == 200, upd.text
    updated = upd.json()
    assert updated["purchase_price"] == "99.00"
    assert updated["selling_price"] == "100.10"
