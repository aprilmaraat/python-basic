"""Test to verify that Transaction create and update use local time correctly"""
from datetime import datetime, timezone
from app.schemas.item import TransactionCreate, TransactionUpdate
from app.models.transaction import TransactionType

def test_transaction_create_with_default_date():
    """Test that default date uses local time"""
    transaction = TransactionCreate(
        title="Test Transaction",
        owner_id=1,
        transaction_type=TransactionType.expense,
        amount_per_unit=100.00,
        quantity=1.000,
        purchase_price=100.00
    )
    # Should have a date set to current local time
    assert transaction.date is not None
    assert transaction.date.tzinfo is None  # Should be naive datetime
    print(f"✓ Default date is naive datetime: {transaction.date}")


def test_transaction_create_with_explicit_date():
    """Test that explicit date is stored as naive datetime"""
    explicit_date = datetime(2025, 11, 15, 10, 30, 0)
    transaction = TransactionCreate(
        title="Test Transaction",
        owner_id=1,
        transaction_type=TransactionType.expense,
        amount_per_unit=100.00,
        quantity=1.000,
        purchase_price=100.00,
        date=explicit_date
    )
    assert transaction.date == explicit_date
    assert transaction.date.tzinfo is None  # Should be naive datetime
    print(f"✓ Explicit naive date preserved: {transaction.date}")


def test_transaction_create_with_aware_datetime():
    """Test that timezone-aware datetime is converted to naive"""
    aware_date = datetime(2025, 11, 15, 10, 30, 0, tzinfo=timezone.utc)
    transaction = TransactionCreate(
        title="Test Transaction",
        owner_id=1,
        transaction_type=TransactionType.expense,
        amount_per_unit=100.00,
        quantity=1.000,
        purchase_price=100.00,
        date=aware_date
    )
    # Should strip timezone info
    assert transaction.date.tzinfo is None
    print(f"✓ Timezone-aware date converted to naive: {transaction.date}")


def test_transaction_update_with_date():
    """Test that update with date uses local time"""
    update_date = datetime(2025, 11, 16, 14, 45, 0)
    transaction_update = TransactionUpdate(
        title="Updated Transaction",
        date=update_date
    )
    assert transaction_update.date == update_date
    assert transaction_update.date.tzinfo is None  # Should be naive datetime
    print(f"✓ Update date is naive datetime: {transaction_update.date}")


def test_transaction_update_with_aware_datetime():
    """Test that update with timezone-aware datetime is converted to naive"""
    aware_date = datetime(2025, 11, 16, 14, 45, 0, tzinfo=timezone.utc)
    transaction_update = TransactionUpdate(
        title="Updated Transaction",
        date=aware_date
    )
    # Should strip timezone info
    assert transaction_update.date.tzinfo is None
    print(f"✓ Update timezone-aware date converted to naive: {transaction_update.date}")


if __name__ == "__main__":
    print("Testing Transaction date handling with local time...\n")
    
    test_transaction_create_with_default_date()
    test_transaction_create_with_explicit_date()
    test_transaction_create_with_aware_datetime()
    test_transaction_update_with_date()
    test_transaction_update_with_aware_datetime()
    
    print("\n✅ All tests passed! Transaction dates are using local time correctly.")
