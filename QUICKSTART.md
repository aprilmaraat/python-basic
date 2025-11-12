# Quick Start: Decimal Quantity Migration

## TL;DR

```powershell
# Run this one command to migrate:
python scripts\migrate_quantity_to_decimal.py

# Then test it works:
pytest tests/test_transaction_decimal_quantity.py -v
```

## What It Does
- ✅ Backs up your database automatically
- ✅ Converts quantity field from INT to DECIMAL
- ✅ Restores all your data
- ✅ Now supports quantities like 2.5, 10.75, 0.333

## New Features
```json
{
  "quantity": 2.5,      // ✅ Now works!
  "quantity": 1.333,    // ✅ Up to 3 decimals
  "quantity": 10,       // ✅ Integers still work
  "total_amount": "..."  // ✅ Auto-calculated correctly
}
```

## Rollback (if needed)
```powershell
# Restore backup database file
Copy-Item "backups\fastapi_backup_*.db" -Destination "fastapi.db" -Force
```

## Files You Care About
- 📝 `MIGRATION_INSTRUCTIONS.md` - Full step-by-step guide
- 📝 `DECIMAL_QUANTITY_CHANGES.md` - Complete technical details
- 📝 `scripts/MIGRATION_README.md` - Migration process docs
- 🔧 `scripts/migrate_quantity_to_decimal.py` - Main migration script
- 📁 `backups/` - All your data backups

## That's It!
Your data is safe. The migration is reversible. Everything is documented.
