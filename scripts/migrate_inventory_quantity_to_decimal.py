"""
Migration script: Convert inventory.quantity field from Integer to Decimal
This script orchestrates the entire migration process:
1. Backup current database
2. Update schema to support decimal quantities
3. Recreate database
4. Restore data with conversions
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import shutil

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def main():
    print("=" * 70)
    print("DATABASE MIGRATION: Inventory Integer quantity → Decimal quantity")
    print("=" * 70)
    print()
    
    db_path = Path(__file__).parent.parent / "fastapi.db"
    backup_dir = Path(__file__).parent.parent / "backups"
    backup_dir.mkdir(exist_ok=True)
    
    # Check if database exists
    if not db_path.exists():
        print("⚠ No existing database found. Proceeding with fresh setup.")
        response = input("Create new database? (y/n): ").lower()
        if response != 'y':
            print("Migration cancelled.")
            return
        
        # Just create the new database
        print("\n✓ Creating fresh database with decimal quantity support...")
        from app.db.session import Base, engine
        from main import enforce_columns
        
        Base.metadata.create_all(bind=engine)
        with engine.connect() as conn:
            enforce_columns(conn)
        
        print("✓ Database created successfully!")
        print("\nYou can now seed the database with: python main.py or POST /seed")
        return
    
    print(f"Current database: {db_path}")
    print()
    
    # Step 1: Backup
    print("Step 1: Backing up current database...")
    print("-" * 70)
    
    try:
        from scripts.backup_database import backup_database
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_before_inventory_decimal_migration_{timestamp}.json"
        backup_path = backup_database(backup_filename)
        
        # Also create a copy of the database file itself
        db_backup_path = backup_dir / f"fastapi_backup_{timestamp}.db"
        shutil.copy2(db_path, db_backup_path)
        print(f"✓ Database file backed up: {db_backup_path}")
        
    except Exception as e:
        print(f"✗ Backup failed: {e}")
        print("\nMigration aborted to protect your data.")
        return
    
    print()
    input("Press Enter to continue with schema changes...")
    print()
    
    # Step 2: Delete old database
    print("Step 2: Removing old database...")
    print("-" * 70)
    try:
        os.remove(db_path)
        print(f"✓ Old database removed: {db_path}")
    except Exception as e:
        print(f"✗ Failed to remove database: {e}")
        return
    
    # Step 3: Create new database with updated schema
    print("\nStep 3: Creating new database with decimal inventory quantity support...")
    print("-" * 70)
    try:
        from app.db.session import Base, engine
        from main import enforce_columns
        
        Base.metadata.create_all(bind=engine)
        with engine.connect() as conn:
            enforce_columns(conn)
        
        print("✓ New database created with decimal inventory quantity support!")
    except Exception as e:
        print(f"✗ Failed to create new database: {e}")
        print("\nYou can restore from backup using:")
        print(f"  python scripts/restore_database.py {backup_path}")
        return
    
    # Step 4: Restore data
    print("\nStep 4: Restoring data from backup...")
    print("-" * 70)
    try:
        from scripts.restore_database import restore_database
        restore_database(str(backup_path))
        print("✓ Data restored successfully!")
    except Exception as e:
        print(f"✗ Data restoration failed: {e}")
        print("\nYou can try manual restoration with:")
        print(f"  python scripts/restore_database.py {backup_path}")
        return
    
    # Step 5: Verify migration
    print("\nStep 5: Verifying migration...")
    print("-" * 70)
    try:
        from sqlalchemy import inspect, text
        from app.db.session import engine
        
        with engine.connect() as conn:
            inspector = inspect(conn)
            columns = inspector.get_columns('inventory')
            qty_col = next((c for c in columns if c['name'] == 'quantity'), None)
            
            if qty_col:
                col_type = str(qty_col['type'])
                print(f"✓ Inventory quantity column type: {col_type}")
                
                # Check if it's a numeric type
                if 'NUMERIC' in col_type.upper() or 'DECIMAL' in col_type.upper():
                    print("✓ Column type is correct (NUMERIC/DECIMAL)")
                else:
                    print(f"⚠ Warning: Column type may not be decimal: {col_type}")
            else:
                print("✗ Quantity column not found!")
            
            # Count records
            result = conn.execute(text("SELECT COUNT(*) FROM inventory"))
            count = result.scalar()
            print(f"✓ Inventory records in database: {count}")
            
    except Exception as e:
        print(f"⚠ Verification warning: {e}")
    
    print()
    print("=" * 70)
    print("MIGRATION COMPLETE!")
    print("=" * 70)
    print()
    print("Summary:")
    print(f"  - Backup created: {backup_path}")
    print(f"  - Database backup: {db_backup_path}")
    print(f"  - Schema updated: inventory.quantity is now NUMERIC(10, 3)")
    print(f"  - Data restored from backup")
    print()
    print("Next steps:")
    print("  1. Test your application")
    print("  2. Verify inventory quantities are working correctly")
    print("  3. If issues occur, restore from backup:")
    print(f"     python scripts/restore_database.py {backup_path}")
    print()


if __name__ == "__main__":
    main()
