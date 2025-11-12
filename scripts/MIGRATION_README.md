# Database Migration: Quantity Field to Decimal

## Overview
This migration converts the `quantity` field in the `transactions` table from `INTEGER` to `NUMERIC(10, 3)` to support decimal quantities like 2.5, 10.75, etc.

## Files Created
- `scripts/backup_database.py` - Exports all database data to JSON
- `scripts/restore_database.py` - Imports data from JSON backup
- `scripts/migrate_quantity_to_decimal.py` - Orchestrates the entire migration process

## Migration Process

### Automatic Migration (Recommended)
Run the migration script which handles everything automatically:

```bash
python scripts/migrate_quantity_to_decimal.py
```

This will:
1. ✅ Backup current database to `backups/backup_before_decimal_migration_YYYYMMDD_HHMMSS.json`
2. ✅ Create a copy of the database file as `backups/fastapi_backup_YYYYMMDD_HHMMSS.db`
3. ✅ Remove the old database
4. ✅ Create new database with decimal quantity support
5. ✅ Restore all data with proper type conversions

### Manual Backup (If Needed)
To manually backup the database:

```bash
python scripts/backup_database.py [optional_filename.json]
```

To manually restore from a backup:

```bash
python scripts/restore_database.py backup_filename.json
```

## Safety Features
- **Dual Backup**: Both JSON export and database file copy
- **Interactive Prompts**: Confirmation before destructive operations
- **Error Handling**: Migration aborts on errors to protect data
- **Detailed Logging**: Clear progress and status messages

## Backup Location
All backups are stored in the `backups/` directory at the project root.

## What Changes
- Transaction `quantity` field now accepts decimals (up to 3 decimal places)
- Examples: `1.5`, `2.75`, `10.333`
- Integer values still work: `1`, `5`, `10`

## Rollback
If something goes wrong, you can:
1. Restore the database file backup: Copy `backups/fastapi_backup_*.db` to `fastapi.db`
2. Or use the restoration script with the JSON backup

## Testing After Migration
Run the test suite to ensure everything works:

```bash
pytest tests/
```

## Notes
- The migration preserves all existing data
- Integer quantities are automatically converted to decimals
- All IDs and relationships are maintained
