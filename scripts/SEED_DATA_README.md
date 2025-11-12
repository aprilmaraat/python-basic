# Seed Data Scripts

This directory contains seed data scripts for initializing the database with sample data.

## Available Seed Scripts

### `seed_transactions.py`

Seeds the transactions table with real transaction data extracted from the database backup on 2025-11-12.

**Usage:**

```bash
# Add seed data (skips existing records)
python scripts/seed_transactions.py

# Clear existing transactions and reseed
python scripts/seed_transactions.py --clear
```

**Data included:**
- 11 transaction records
- All transactions are of type "earning" (customer purchases)
- Transactions reference:
  - User ID: 1 (DB Wholesale Trading)
  - Various inventory items (Butane, Coca-Cola, etc.)
- Transaction data includes:
  - Title and description
  - Amount per unit, quantity, and purchase price
  - Transaction date (2025-11-12)
  - Inventory item references

## Database Backups

All database backups are stored in the `backups/` directory with timestamps.

**Latest backup:** `backup_20251112.json`

Contains:
- 1 user
- 5 categories
- 10 weight types
- 12 inventory items
- 11 transactions

## Restoring from Backup

To restore the database from a backup:

```bash
python scripts/restore_database.py backups/backup_20251112.json
```

## Creating New Backups

To create a new database backup:

```bash
# Auto-generated filename with timestamp
python scripts/backup_database.py

# Custom filename
python scripts/backup_database.py "my_backup.json"
```
