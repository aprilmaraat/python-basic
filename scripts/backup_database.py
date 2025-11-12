"""
Database backup script - Exports all data to JSON before schema changes.
"""
import json
import sys
from pathlib import Path
from datetime import datetime, date
from decimal import Decimal

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.session import SessionLocal, engine
from app.models.user import User
from app.models.category import Category
from app.models.weight import Weight
from app.models.inventory import Inventory
from app.models.transaction import Transaction
from sqlalchemy import inspect, select


def decimal_date_serializer(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def backup_database(backup_file: str = None):
    """Backup all database tables to a JSON file."""
    if backup_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"database_backup_{timestamp}.json"
    
    backup_path = Path(__file__).parent.parent / "backups" / backup_file
    backup_path.parent.mkdir(exist_ok=True)
    
    db = SessionLocal()
    try:
        # Check if tables exist
        inspector = inspect(engine)
        if not inspector.has_table('users'):
            print("No database tables found. Nothing to backup.")
            return None
        
        backup_data = {
            "timestamp": datetime.now().isoformat(),
            "users": [],
            "categories": [],
            "weights": [],
            "inventory": [],
            "transactions": []
        }
        
        # Backup users
        users = db.scalars(select(User)).all()
        for user in users:
            backup_data["users"].append({
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "is_active": user.is_active
            })
        
        # Backup categories
        categories = db.scalars(select(Category)).all()
        for cat in categories:
            backup_data["categories"].append({
                "id": cat.id,
                "name": cat.name
            })
        
        # Backup weights
        weights = db.scalars(select(Weight)).all()
        for weight in weights:
            backup_data["weights"].append({
                "id": weight.id,
                "name": weight.name
            })
        
        # Backup inventory
        inventories = db.scalars(select(Inventory)).all()
        for inv in inventories:
            inv_data = {
                "id": inv.id,
                "name": inv.name,
                "shortname": inv.shortname,
                "quantity": inv.quantity,
                "category_id": inv.category_id,
                "weight_id": inv.weight_id
            }
            # Add optional fields if they exist
            if hasattr(inv, 'purchase_price'):
                inv_data["purchase_price"] = str(inv.purchase_price)
            if hasattr(inv, 'selling_price'):
                inv_data["selling_price"] = str(inv.selling_price)
            backup_data["inventory"].append(inv_data)
        
        # Backup transactions
        transactions = db.scalars(select(Transaction)).all()
        for trans in transactions:
            backup_data["transactions"].append({
                "id": trans.id,
                "title": trans.title,
                "description": trans.description,
                "owner_id": trans.owner_id,
                "transaction_type": trans.transaction_type.value,
                "amount_per_unit": str(trans.amount_per_unit),
                "quantity": trans.quantity,  # Will be int or Decimal
                "purchase_price": str(trans.purchase_price),
                "date": trans.date.isoformat(),
                "inventory_id": trans.inventory_id
            })
        
        # Write to file
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, default=decimal_date_serializer)
        
        print(f"✓ Database backup created: {backup_path}")
        print(f"  - Users: {len(backup_data['users'])}")
        print(f"  - Categories: {len(backup_data['categories'])}")
        print(f"  - Weights: {len(backup_data['weights'])}")
        print(f"  - Inventory: {len(backup_data['inventory'])}")
        print(f"  - Transactions: {len(backup_data['transactions'])}")
        
        return str(backup_path)
    
    except Exception as e:
        print(f"✗ Error during backup: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    backup_file = sys.argv[1] if len(sys.argv) > 1 else None
    backup_database(backup_file)
