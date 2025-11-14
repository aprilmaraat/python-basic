"""
Database restoration script - Imports data from JSON backup after schema changes.
"""
import json
import sys
from pathlib import Path
from datetime import datetime
from decimal import Decimal

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.session import SessionLocal, Base, engine
from app.models.user import User
from app.models.category import Category
from app.models.weight import Weight
from app.models.inventory import Inventory
from app.models.transaction import Transaction, TransactionType
from sqlalchemy import text


def restore_database(backup_file: str):
    """Restore database from a JSON backup file."""
    backup_path = Path(backup_file)
    
    if not backup_path.exists():
        # Try relative to backups directory
        backup_path = Path(__file__).parent.parent / "backups" / backup_file
    
    if not backup_path.exists():
        print(f"✗ Backup file not found: {backup_file}")
        return False
    
    print(f"Restoring from: {backup_path}")
    
    with open(backup_path, 'r', encoding='utf-8') as f:
        backup_data = json.load(f)
    
    db = SessionLocal()
    try:
        # Restore users
        for user_data in backup_data.get("users", []):
            user = User(
                id=user_data["id"],
                email=user_data["email"],
                full_name=user_data["full_name"],
                is_active=user_data["is_active"]
            )
            db.add(user)
        db.commit()
        
        # Restore categories
        for cat_data in backup_data.get("categories", []):
            category = Category(
                id=cat_data["id"],
                name=cat_data["name"]
            )
            db.add(category)
        db.commit()
        
        # Restore weights
        for weight_data in backup_data.get("weights", []):
            weight = Weight(
                id=weight_data["id"],
                name=weight_data["name"]
            )
            db.add(weight)
        db.commit()
        
        # Restore inventory
        for inv_data in backup_data.get("inventory", []):
            inv_dict = {
                "id": inv_data["id"],
                "name": inv_data["name"],
                "shortname": inv_data.get("shortname"),
                "quantity": inv_data["quantity"],
                "category_id": inv_data["category_id"],
                "weight_id": inv_data["weight_id"]
            }
            # Add optional fields if they exist in the backup
            if "purchase_price" in inv_data:
                inv_dict["purchase_price"] = Decimal(inv_data["purchase_price"])
            if "selling_price" in inv_data:
                inv_dict["selling_price"] = Decimal(inv_data["selling_price"])
            
            inventory = Inventory(**inv_dict)
            db.add(inventory)
        db.commit()
        
        # Restore transactions (with decimal quantity support)
        for trans_data in backup_data.get("transactions", []):
            # Convert quantity to Decimal
            quantity = trans_data["quantity"]
            if isinstance(quantity, (int, float)):
                quantity = Decimal(str(quantity))
            elif isinstance(quantity, str):
                quantity = Decimal(quantity)
            
            # Parse datetime, handling both date-only and datetime formats
            date_value = trans_data["date"]
            if 'T' in date_value or ' ' in date_value:
                # Already a datetime string
                parsed_date = datetime.fromisoformat(date_value)
            else:
                # Date-only string, convert to datetime at midnight
                parsed_date = datetime.fromisoformat(date_value + "T00:00:00")
            
            transaction = Transaction(
                id=trans_data["id"],
                title=trans_data["title"],
                description=trans_data.get("description"),
                owner_id=trans_data["owner_id"],
                transaction_type=TransactionType(trans_data["transaction_type"]),
                amount_per_unit=Decimal(trans_data["amount_per_unit"]),
                quantity=quantity,
                purchase_price=Decimal(trans_data["purchase_price"]),
                date=parsed_date,
                inventory_id=trans_data.get("inventory_id")
            )
            db.add(transaction)
        db.commit()
        
        # Reset SQLite sequences
        with engine.connect() as conn:
            tables = ["users", "categories", "weights", "inventory", "transactions"]
            for table in tables:
                result = conn.execute(text(f"SELECT MAX(id) FROM {table}"))
                max_id = result.scalar() or 0
                conn.execute(text(f"UPDATE sqlite_sequence SET seq = {max_id} WHERE name = '{table}'"))
                conn.commit()
        
        print(f"✓ Database restored successfully")
        print(f"  - Users: {len(backup_data.get('users', []))}")
        print(f"  - Categories: {len(backup_data.get('categories', []))}")
        print(f"  - Weights: {len(backup_data.get('weights', []))}")
        print(f"  - Inventory: {len(backup_data.get('inventory', []))}")
        print(f"  - Transactions: {len(backup_data.get('transactions', []))}")
        
        return True
    
    except Exception as e:
        print(f"✗ Error during restoration: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python restore_database.py <backup_file>")
        sys.exit(1)
    
    restore_database(sys.argv[1])
