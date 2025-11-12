"""
Migration script: Convert quantity field from Integer to Decimal
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
    print("DATABASE MIGRATION: Integer quantity → Decimal quantity")
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
        backup_filename = f"backup_before_decimal_migration_{timestamp}.json"
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
    print("\nStep 3: Creating new database with decimal quantity support...")
    print("-" * 70)
    try:
        from app.db.session import Base, engine
        from main import enforce_columns
        
        Base.metadata.create_all(bind=engine)
        with engine.connect() as conn:
            enforce_columns(conn)
        
        print("✓ New database created with decimal quantity support!")
    except Exception as e:
        print(f"✗ Failed to create new database: {e}")
        print(f"\n⚠ You can restore from backup: {db_backup_path}")
        return
    
    # Step 4: Restore data
    print("\nStep 4: Restoring data from backup...")
    print("-" * 70)
    try:
        from scripts.restore_database import restore_database
        restore_database(backup_path)
    except Exception as e:
        print(f"✗ Data restoration failed: {e}")
        print(f"\n⚠ Database file backup available at: {db_backup_path}")
        print(f"⚠ JSON backup available at: {backup_path}")
        return
    
    print()
    print("=" * 70)
    print("✓ MIGRATION COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print()
    print("Summary:")
    print(f"  - Backup files saved in: {backup_dir}")
    print(f"  - Database JSON backup: {backup_filename}")
    print(f"  - Database file backup: {db_backup_path.name}")
    print()
    print("The quantity field now supports decimal values (up to 3 decimal places)")
    print("You can now use values like 2.5, 10.75, etc. for quantities.")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Migration cancelled by user.")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
