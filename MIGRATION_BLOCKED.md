# MIGRATION BLOCKED: Database File In Use

## Problem
The migration script cannot proceed because the database file (`fastapi.db`) is currently locked by another process.

## ✅ Good News
Your data has been successfully backed up:
- JSON backup: `backups/backup_before_decimal_migration_20251110_213029.json`
- Database file backup: `backups/fastapi_backup_20251110_213029.db`

## Solution: Close All Database Connections

### Step 1: Stop Any Running Servers
If you have the FastAPI server running, stop it:
- Press `Ctrl+C` in the terminal where `uvicorn` is running
- Or close any terminals running `python main.py` or similar

### Step 2: Close Any Database Connections
Check for and close:
- Any Python shells or notebooks accessing the database
- Any database browser tools (DB Browser for SQLite, etc.)
- Any running pytest processes

### Step 3: Verify No Python Processes
In PowerShell, check for Python processes:
```powershell
Get-Process python* | Stop-Process -Force
```

### Step 4: Rerun Migration
Once all processes are stopped:
```powershell
python scripts\migrate_quantity_to_decimal.py
```

The migration will:
1. ✅ Skip the backup step (already done!)
2. ✅ Delete old database
3. ✅ Create new database with decimal support
4. ✅ Restore your data

## Alternative: Manual Migration Steps

If you prefer to do it manually:

### 1. Stop all database connections (see above)

### 2. Backup current database (already done! ✅)

### 3. Delete old database
```powershell
Remove-Item fastapi.db -Force
```

### 4. Recreate database with new schema
```powershell
python -c "from app.db.session import Base, engine; from main import enforce_columns; Base.metadata.create_all(bind=engine); from sqlalchemy import create_engine; conn = engine.connect(); enforce_columns(conn); conn.close()"
```

### 5. Restore data
```powershell
python scripts\restore_database.py backups\backup_before_decimal_migration_20251110_213029.json
```

### 6. Verify with tests
```powershell
pytest tests/test_transaction_decimal_quantity.py -v
```

## Need to Rollback?

If you want to go back to the original database:
```powershell
# Delete current database
Remove-Item fastapi.db -Force

# Restore from backup
Copy-Item backups\fastapi_backup_20251110_213029.db fastapi.db
```

## Summary

**Your data is safe!** The migration has backed up everything. You just need to:
1. Close any processes using the database
2. Rerun the migration script

The backup files will remain in the `backups/` folder for safety.
