# Instructions: Running the Quantity to Decimal Migration

## ⚠️ IMPORTANT: Before Running Migration

This migration will convert the `quantity` field from INTEGER to DECIMAL. All your existing data will be automatically backed up and restored.

## Step-by-Step Instructions

### 1. Ensure Python Environment is Active
Make sure you're in the correct Python environment with all dependencies installed:

```powershell
# If using a virtual environment, activate it first
# Then verify dependencies
pip install -r requirements.txt
```

### 2. Run the Migration Script
Execute the main migration script which handles everything automatically:

```powershell
python scripts\migrate_quantity_to_decimal.py
```

**What this does:**
- ✅ Checks if database exists
- ✅ Creates JSON backup of all data
- ✅ Creates a copy of the database file
- ✅ Prompts for confirmation (you can review backups before proceeding)
- ✅ Removes old database
- ✅ Creates new database with decimal support
- ✅ Restores all your data automatically

### 3. Verify Migration Success
After migration completes, verify the changes:

```powershell
# Run all tests
pytest tests/

# Or run specific decimal quantity tests
pytest tests/test_transaction_decimal_quantity.py -v
```

### 4. Test the API
Start the application and test with decimal quantities:

```powershell
# Start the server
uvicorn main:app --reload

# In another terminal or using Postman/curl, test creating a transaction:
# POST http://localhost:8000/transactions
# Body:
{
  "title": "Test Decimal",
  "owner_id": 1,
  "transaction_type": "expense",
  "amount_per_unit": "100.00",
  "quantity": 2.5,
  "date": "2025-11-07"
}
```

## If You Don't Have an Existing Database

If you're starting fresh or the database doesn't exist:

1. The migration script will detect this
2. It will offer to create a new database
3. Type `y` to confirm
4. Then seed the database:
   ```powershell
   # Option 1: Via API
   curl -X POST http://localhost:8000/seed
   
   # Option 2: Directly in Python
   python -c "from main import SessionLocal, seed; db = SessionLocal(); seed(db); db.close()"
   ```

## Backup Locations

All backups are saved in the `backups/` directory:
- `backup_before_decimal_migration_YYYYMMDD_HHMMSS.json` - JSON export of all data
- `fastapi_backup_YYYYMMDD_HHMMSS.db` - Copy of original database file

## Rollback Procedure

If something goes wrong and you need to restore:

### Option 1: Restore Database File
```powershell
# Copy the backup database file
Copy-Item "backups\fastapi_backup_YYYYMMDD_HHMMSS.db" -Destination "fastapi.db" -Force
```

### Option 2: Restore from JSON
```powershell
# First delete the current database
Remove-Item "fastapi.db" -Force

# Recreate fresh database (code should already be updated)
python -c "from app.db.session import Base, engine; Base.metadata.create_all(bind=engine)"

# Restore from JSON backup
python scripts\restore_database.py backups\backup_before_decimal_migration_YYYYMMDD_HHMMSS.json
```

## What Changed?

### Before
```python
"quantity": 2  # Integer only
```

### After
```python
"quantity": 2.5   # Decimals supported!
"quantity": 1.333 # Up to 3 decimal places
"quantity": 10    # Integers still work
```

### Total Amount Calculation
```python
# Example: 2.5 units at $100 each
amount_per_unit: 100.00
quantity: 2.5
total_amount: 250.00  # Automatically calculated
```

## Files Modified

- ✅ `app/models/transaction.py` - Database model
- ✅ `app/schemas/item.py` - Pydantic schemas
- ✅ `app/crud/item.py` - CRUD operations
- ✅ `main.py` - Database initialization
- ✅ `tests/test_transaction_filtering.py` - Updated test
- ✅ `tests/test_transaction_decimal_quantity.py` - New comprehensive tests

## New Files Created

- ✅ `scripts/backup_database.py` - Backup utility
- ✅ `scripts/restore_database.py` - Restore utility
- ✅ `scripts/migrate_quantity_to_decimal.py` - Main migration script
- ✅ `scripts/MIGRATION_README.md` - Detailed migration docs
- ✅ `DECIMAL_QUANTITY_CHANGES.md` - Complete change summary

## Testing

After migration, run the full test suite:

```powershell
# Run all tests
pytest tests/ -v

# Run only decimal quantity tests
pytest tests/test_transaction_decimal_quantity.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

## Need Help?

If you encounter any issues:

1. Check the backup files in `backups/` directory
2. Review `DECIMAL_QUANTITY_CHANGES.md` for detailed changes
3. Check `scripts/MIGRATION_README.md` for migration details
4. Restore from backup if needed (see Rollback Procedure above)

## Summary

This migration is **safe** and **reversible**:
- ✅ Automatic backups before any changes
- ✅ All data preserved and restored
- ✅ Backward compatible (integers still work)
- ✅ Comprehensive test coverage
- ✅ Easy rollback if needed

**The quantity field now supports decimal values like 2.5, 10.75, 0.333, etc., while still accepting integer values for backward compatibility!**
