"""
Database migration script - Converts date column to datetime in transactions table.
This migration converts existing date values (DATE type) to datetime values (DATETIME type).
"""
import sys
from pathlib import Path
from datetime import datetime
import shutil

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.session import engine
from sqlalchemy import text, inspect


def migrate_date_to_datetime():
    """
    Migrate the date column from DATE to DATETIME.
    This is done by altering the column type in SQLite.
    """
    print("=" * 70)
    print("MIGRATION: Date → DateTime in transactions table")
    print("=" * 70)
    print()
    
    # First, create a backup
    print("Step 1: Creating backup...")
    print("-" * 70)
    try:
        from scripts.backup_database import backup_database
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_before_datetime_migration_{timestamp}.json"
        backup_path = backup_database(backup_filename)
        
        # Also backup the database file itself
        db_path = Path(__file__).parent.parent / "fastapi.db"
        if db_path.exists():
            backup_dir = Path(__file__).parent.parent / "backups"
            backup_dir.mkdir(exist_ok=True)
            db_backup_path = backup_dir / f"fastapi_backup_{timestamp}.db"
            shutil.copy2(db_path, db_backup_path)
            print(f"✓ Database file backed up: {db_backup_path}")
        print()
    except Exception as e:
        print(f"✗ Backup failed: {e}")
        print("\nMigration aborted to protect your data.")
        return False
    
    input("Press Enter to continue with schema changes...")
    print()
    
    # Step 2: Alter the table
    print("Step 2: Migrating date column to datetime...")
    print("-" * 70)
    
    with engine.connect() as conn:
        inspector = inspect(engine)
        
        # Check if transactions table exists
        if not inspector.has_table('transactions'):
            print("✗ Transactions table does not exist.")
            return False
        
        # In SQLite, we need to recreate the table to change column type
        # SQLite doesn't support ALTER COLUMN TYPE directly
        
        try:
            # Begin transaction
            trans = conn.begin()
            
            # Create a temporary table with the new schema
            conn.execute(text("""
                CREATE TABLE transactions_new (
                    id INTEGER PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description VARCHAR(1024),
                    owner_id INTEGER NOT NULL,
                    transaction_type TEXT NOT NULL,
                    amount NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
                    quantity NUMERIC(10, 3) NOT NULL DEFAULT 1.000,
                    purchase_price NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
                    inventory_id INTEGER,
                    date DATETIME NOT NULL,
                    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (inventory_id) REFERENCES inventory(id) ON DELETE SET NULL
                )
            """))
            
            # Copy data from old table to new table
            # Convert DATE to DATETIME by appending time portion
            conn.execute(text("""
                INSERT INTO transactions_new 
                    (id, title, description, owner_id, transaction_type, amount, quantity, purchase_price, inventory_id, date)
                SELECT 
                    id, title, description, owner_id, transaction_type, amount, quantity, purchase_price, inventory_id,
                    datetime(date) as date
                FROM transactions
            """))
            
            # Drop old table
            conn.execute(text("DROP TABLE transactions"))
            
            # Rename new table to original name
            conn.execute(text("ALTER TABLE transactions_new RENAME TO transactions"))
            
            # Recreate indexes
            conn.execute(text("CREATE INDEX ix_transactions_id ON transactions (id)"))
            conn.execute(text("CREATE INDEX ix_transactions_title ON transactions (title)"))
            conn.execute(text("CREATE INDEX ix_transactions_owner_id ON transactions (owner_id)"))
            conn.execute(text("CREATE INDEX ix_transactions_inventory_id ON transactions (inventory_id)"))
            
            # Commit transaction
            trans.commit()
            
            print("✓ Successfully migrated date column to datetime")
            print()
            
        except Exception as e:
            trans.rollback()
            print(f"✗ Migration failed: {e}")
            print("\nYou can restore from the backup if needed.")
            return False
    
    print("=" * 70)
    print("MIGRATION COMPLETE!")
    print("=" * 70)
    print()
    print("✓ The date column is now DATETIME type")
    print("✓ All existing dates have been converted to datetime (midnight)")
    print("✓ Backup saved:", backup_path)
    print()
    
    return True


if __name__ == "__main__":
    success = migrate_date_to_datetime()
    sys.exit(0 if success else 1)
