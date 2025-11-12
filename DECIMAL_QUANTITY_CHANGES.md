# Summary: Quantity Field Migration to Decimal

## Changes Overview
Converted the `quantity` field in transactions from `INTEGER` to `NUMERIC(10, 3)` to support decimal quantities like 2.5, 10.75, etc.

## Files Modified

### 1. **Database Model** (`app/models/transaction.py`)
- Changed `quantity: Mapped[int]` to `quantity: Mapped[Decimal]`
- Updated column type from `Integer` to `Numeric(10, 3)`
- Default value changed from `1` to `Decimal('1.000')`
- Updated `total_amount` hybrid property to handle Decimal quantities

### 2. **Schemas** (`app/schemas/item.py`)
- Changed `quantity` type from `int` to `Decimal` in all transaction schemas:
  - `TransactionBase`
  - `TransactionUpdate`
  - `TransactionRead`
  - `TransactionReadSimple`
  - `TransactionReadDetailed`
- Added separate validators for quantity (3 decimal places) vs money fields (2 decimal places)
- Default quantity changed to `Decimal('1.000')`

### 3. **CRUD Operations** (`app/crud/item.py`)
- Updated `create()` to convert quantity to Decimal
- Updated `update()` to handle quantity as Decimal in conversions

### 4. **Database Initialization** (`main.py`)
- Updated `enforce_columns()` to use `NUMERIC(10, 3) DEFAULT 1.000` for quantity

### 5. **Tests**
- **Modified**: `tests/test_transaction_filtering.py`
  - Updated to test with decimal quantity (2.5)
  - Updated assertions to handle Decimal comparisons
  
- **Created**: `tests/test_transaction_decimal_quantity.py`
  - Comprehensive decimal quantity tests
  - Tests for various fractional values (0.5, 1.333, 99.999)
  - Backward compatibility tests (integer quantities still work)
  - Precision tests (up to 3 decimal places)

## Migration Scripts Created

### 1. `scripts/backup_database.py`
- Exports all database tables to JSON
- Preserves all data including users, categories, weights, inventory, and transactions
- Handles Decimal and date serialization

### 2. `scripts/restore_database.py`
- Imports data from JSON backup
- Converts quantities to Decimal automatically
- Resets SQLite sequences to maintain ID continuity

### 3. `scripts/migrate_quantity_to_decimal.py`
- **Main migration orchestrator**
- Performs complete migration process:
  1. Checks for existing database
  2. Creates JSON backup of all data
  3. Creates copy of database file
  4. Removes old database
  5. Creates new database with decimal support
  6. Restores all data
- Interactive with safety prompts
- Comprehensive error handling

### 4. `scripts/MIGRATION_README.md`
- Complete documentation of migration process
- Usage instructions
- Safety features explanation
- Rollback procedures

## Key Features

### Decimal Support
- Quantities support up to 3 decimal places (e.g., 2.125, 0.5, 10.333)
- Money fields (amount_per_unit, purchase_price) remain at 2 decimal places
- Automatic rounding using ROUND_HALF_UP

### Backward Compatibility
- Integer quantities still work (automatically converted to Decimal)
- Existing data preserved through migration
- API endpoints unchanged

### Data Safety
- Automatic backup before any schema changes
- Dual backup strategy (JSON + database file copy)
- All backups timestamped and stored in `backups/` directory
- Interactive prompts prevent accidental data loss
- Easy rollback if needed

### Calculations
- `total_amount` correctly calculated as `amount_per_unit * quantity`
- Works with both integer and decimal quantities
- Proper Decimal arithmetic to avoid floating-point issues

## Usage Examples

### Creating Transaction with Decimal Quantity
```python
{
    "title": "Purchase LPG",
    "owner_id": 1,
    "transaction_type": "expense",
    "amount_per_unit": "100.00",
    "quantity": 2.5,  # Decimal quantity
    "date": "2025-11-07"
}
# total_amount will be 250.00 (100.00 * 2.5)
```

### Integer Still Works
```python
{
    "title": "Purchase Items",
    "owner_id": 1,
    "amount_per_unit": "50.00",
    "quantity": 10,  # Integer automatically converts to Decimal
}
# quantity stored as 10.000, total_amount = 500.00
```

## Running the Migration

### Option 1: Automated Migration (Recommended)
```bash
python scripts/migrate_quantity_to_decimal.py
```

### Option 2: Manual Steps
```bash
# 1. Backup
python scripts/backup_database.py

# 2. Delete database
# (handled by migration script)

# 3. Update code
# (all code already updated)

# 4. Restore data
python scripts/restore_database.py <backup_file.json>
```

## Testing
Run the test suite to verify everything works:
```bash
pytest tests/
```

## Rollback Procedure
If issues occur, restore from backup:
1. Copy `backups/fastapi_backup_TIMESTAMP.db` to `fastapi.db`
2. Or run: `python scripts/restore_database.py <backup_file.json>`

## Notes
- All existing data is preserved
- Transaction IDs maintained
- Relationships unchanged
- API behavior consistent
- Performance impact negligible
