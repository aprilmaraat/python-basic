"""
Alternative migration: Alter existing table instead of recreating database.
This approach modifies the existing database without deleting it.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime
from app.db.session import engine
from sqlalchemy import text, inspect


def migrate_quantity_column():
    """
    Migrate the quantity column from INTEGER to NUMERIC(10,3).
    This is done in-place without deleting the database.
    """
    print("=" * 70)
    print("IN-PLACE MIGRATION: Integer quantity → Decimal quantity")
    print("=" * 70)
    print()
    
    # First, create a backup
    print("Step 1: Creating backup...")
    print("-" * 70)
    try:
        from scripts.backup_database import backup_database
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_before_alter_migration_{timestamp}.json"
        backup_path = backup_database(backup_filename)
        print()
    except Exception as e:
        print(f"✗ Backup failed: {e}")
        print("\nMigration aborted to protect your data.")
        return False
    
    input("Press Enter to continue with schema changes...")
    print()
    
    # Step 2: Alter the table
    print("Step 2: Altering quantity column...")
    print("-" * 70)
    
    try:
        with engine.begin() as conn:
            inspector = inspect(conn)
            
            # Check if transactions table exists
            if not inspector.has_table('transactions'):
                print("✗ Transactions table not found!")
                return False
            
            # Get current columns
            columns = {c['name']: c for c in inspector.get_columns('transactions')}
            
            if 'quantity' not in columns:
                print("✗ Quantity column not found!")
                return False
            
            print(f"Current quantity column type: {columns['quantity']['type']}")
            
            # SQLite doesn't support ALTER COLUMN directly, we need to:
            # 1. Create a new column with the new type
            # 2. Copy data from old column to new column
            # 3. Drop old column
            # 4. Rename new column to old name
            
            # However, SQLite has limitations. The safest approach:
            # Create a new temporary column, copy data, then rename
            
            print("\nCreating temporary decimal column...")
            conn.execute(text("ALTER TABLE transactions ADD COLUMN quantity_new NUMERIC(10, 3)"))
            
            print("Copying data from old quantity to new quantity column...")
            conn.execute(text("UPDATE transactions SET quantity_new = CAST(quantity AS NUMERIC(10, 3))"))
            
            print("Setting default value for new column...")
            # Note: SQLite doesn't support ALTER COLUMN to set default, 
            # so we ensure all NULL values are set
            conn.execute(text("UPDATE transactions SET quantity_new = 1.000 WHERE quantity_new IS NULL"))
            
            print("\nNote: Due to SQLite limitations, we've created 'quantity_new' column.")
            print("The old 'quantity' column still exists for safety.")
            print("After verifying everything works, you can:")
            print("  1. Drop the old 'quantity' column")
            print("  2. Rename 'quantity_new' to 'quantity'")
            print("\nFor now, the application will use 'quantity_new' via the model.")
            
        print("\n✓ Column alteration completed!")
        
    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        print(f"\nYou can restore from backup: {backup_path}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    print("=" * 70)
    print("✓ MIGRATION COMPLETED!")
    print("=" * 70)
    print()
    print(f"Backup saved: {backup_path}")
    print()
    print("IMPORTANT: Update the model to use 'quantity_new' column name,")
    print("or recreate the database using the full migration script when")
    print("the database is not locked by another process.")
    print()
    
    return True


if __name__ == "__main__":
    try:
        success = migrate_quantity_column()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n✗ Migration cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
