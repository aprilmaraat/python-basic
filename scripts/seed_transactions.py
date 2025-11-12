"""
Seed data for Transactions table
Generated from database backup on 2025-11-12
"""
import sys
from pathlib import Path
from datetime import date
from decimal import Decimal

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.session import SessionLocal
from app.models.transaction import Transaction, TransactionType


# Transaction seed data - from backup_20251112.json
TRANSACTION_SEED_DATA = [
    {
        "id": 1,
        "title": "Customer Purchase",
        "description": None,
        "owner_id": 1,
        "transaction_type": TransactionType.earning,
        "amount_per_unit": Decimal("28.00"),
        "quantity": Decimal("1.000"),
        "purchase_price": Decimal("23.26"),
        "date": date(2025, 11, 12),
        "inventory_id": 2
    },
    {
        "id": 2,
        "title": "Customer Purchase",
        "description": None,
        "owner_id": 1,
        "transaction_type": TransactionType.earning,
        "amount_per_unit": Decimal("650.00"),
        "quantity": Decimal("3.000"),
        "purchase_price": Decimal("640.00"),
        "date": date(2025, 11, 12),
        "inventory_id": 5
    },
    {
        "id": 3,
        "title": "Customer PUrchase",
        "description": None,
        "owner_id": 1,
        "transaction_type": TransactionType.earning,
        "amount_per_unit": Decimal("400.00"),
        "quantity": Decimal("1.000"),
        "purchase_price": Decimal("386.00"),
        "date": date(2025, 11, 12),
        "inventory_id": 3
    },
    {
        "id": 4,
        "title": "Customer Purchase",
        "description": None,
        "owner_id": 1,
        "transaction_type": TransactionType.earning,
        "amount_per_unit": Decimal("194.00"),
        "quantity": Decimal("2.000"),
        "purchase_price": Decimal("181.00"),
        "date": date(2025, 11, 12),
        "inventory_id": 7
    },
    {
        "id": 5,
        "title": "Customer Purchase",
        "description": None,
        "owner_id": 1,
        "transaction_type": TransactionType.earning,
        "amount_per_unit": Decimal("75.00"),
        "quantity": Decimal("2.000"),
        "purchase_price": Decimal("60.00"),
        "date": date(2025, 11, 12),
        "inventory_id": 2
    },
    {
        "id": 6,
        "title": "Customer Purchase",
        "description": None,
        "owner_id": 1,
        "transaction_type": TransactionType.earning,
        "amount_per_unit": Decimal("28.00"),
        "quantity": Decimal("2.000"),
        "purchase_price": Decimal("23.26"),
        "date": date(2025, 11, 12),
        "inventory_id": 2
    },
    {
        "id": 7,
        "title": "Customer Purchase",
        "description": None,
        "owner_id": 1,
        "transaction_type": TransactionType.earning,
        "amount_per_unit": Decimal("28.00"),
        "quantity": Decimal("10.000"),
        "purchase_price": Decimal("23.26"),
        "date": date(2025, 11, 12),
        "inventory_id": 2
    },
    {
        "id": 8,
        "title": "cuatomer purchase",
        "description": None,
        "owner_id": 1,
        "transaction_type": TransactionType.earning,
        "amount_per_unit": Decimal("20.00"),
        "quantity": Decimal("24.000"),
        "purchase_price": Decimal("17.99"),
        "date": date(2025, 11, 12),
        "inventory_id": 6
    },
    {
        "id": 9,
        "title": "customer purchase",
        "description": None,
        "owner_id": 1,
        "transaction_type": TransactionType.earning,
        "amount_per_unit": Decimal("26.00"),
        "quantity": Decimal("21.000"),
        "purchase_price": Decimal("23.26"),
        "date": date(2025, 11, 12),
        "inventory_id": 2
    },
    {
        "id": 10,
        "title": "customer purs",
        "description": None,
        "owner_id": 1,
        "transaction_type": TransactionType.earning,
        "amount_per_unit": Decimal("194.00"),
        "quantity": Decimal("1.000"),
        "purchase_price": Decimal("181.00"),
        "date": date(2025, 11, 12),
        "inventory_id": 7
    },
    {
        "id": 11,
        "title": "customer purchase",
        "description": None,
        "owner_id": 1,
        "transaction_type": TransactionType.earning,
        "amount_per_unit": Decimal("200.00"),
        "quantity": Decimal("0.500"),
        "purchase_price": Decimal("386.00"),
        "date": date(2025, 11, 12),
        "inventory_id": 3
    }
]


def seed_transactions(clear_existing=False):
    """
    Seed the transactions table with initial data.
    
    Args:
        clear_existing: If True, delete all existing transactions before seeding
    """
    db = SessionLocal()
    try:
        if clear_existing:
            print("Clearing existing transactions...")
            db.query(Transaction).delete()
            db.commit()
        
        print(f"Seeding {len(TRANSACTION_SEED_DATA)} transactions...")
        
        for trans_data in TRANSACTION_SEED_DATA:
            # Check if transaction already exists
            existing = db.query(Transaction).filter(Transaction.id == trans_data["id"]).first()
            if existing:
                print(f"  - Transaction ID {trans_data['id']} already exists, skipping...")
                continue
            
            transaction = Transaction(**trans_data)
            db.add(transaction)
            print(f"  ✓ Added: {transaction.title} (ID: {transaction.id})")
        
        db.commit()
        print(f"\n✓ Successfully seeded {len(TRANSACTION_SEED_DATA)} transactions!")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error seeding transactions: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Seed transactions table")
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear existing transactions before seeding"
    )
    
    args = parser.parse_args()
    seed_transactions(clear_existing=args.clear)
