# Setup Instructions for New Machine

This guide will help you set up the FastAPI Expense Tracker on a new computer.

## Prerequisites

- Python 3.13 or higher
- Git installed

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/aprilmaraat/python-basic.git
cd python-basic
```

### 2. Install Dependencies

**Option A: Using setup.bat (Recommended)**
```bash
# Double-click setup.bat or run:
setup.bat
```

**Option B: Manual Installation**
```bash
# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Create Database with Schema

The database will be automatically created when you first run the application, but you can create it manually:

**Option A: Automatic (First Run)**
```bash
# Just start the server - it will create the database automatically
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

**Option B: Manual Creation**
```bash
python -c "from app.db.session import Base, engine; Base.metadata.create_all(bind=engine); print('Database created successfully!')"
```

### 4. Restore Database with Data (Optional)

If you want the same data from your original machine:

**Method 1: Copy the Database File**
```bash
# Copy fastapi.db from your original machine to the new machine
# Place it in the project root directory
```

**Method 2: Restore from JSON Backup**
```bash
# Copy the backup file from backups/ folder to the new machine
python scripts/restore_database.py backups/backup_20251112.json
```

**Method 3: Use Seed Data**
```bash
# This seeds the 11 transactions from the original database
python scripts/seed_transactions.py
```

### 5. Verify Setup

```bash
# Start the server
python -m uvicorn main:app --host 0.0.0.0 --port 8000

# Open browser and go to:
# http://localhost:8000/docs
```

## Quick Commands Reference

### Fresh Install (Empty Database)
```bash
git clone https://github.com/aprilmaraat/python-basic.git
cd python-basic
setup.bat
start_server.bat
```

### Fresh Install + Sample Data
```bash
git clone https://github.com/aprilmaraat/python-basic.git
cd python-basic
setup.bat
python scripts/seed_transactions.py
start_server.bat
```

### Fresh Install + Exact Copy of Your Data
```bash
git clone https://github.com/aprilmaraat/python-basic.git
cd python-basic
setup.bat

# Copy fastapi.db from original machine to here
# OR restore from backup:
python scripts/restore_database.py backups/backup_20251112.json

start_server.bat
```

## Database Migration Notes

- **Database location:** `fastapi.db` (SQLite file in project root)
- **Backups location:** `backups/` folder
- **Schema is auto-created** when the app first runs
- **No data by default** - you need to either:
  - Copy the database file
  - Restore from backup
  - Use seed data
  - Create new data via API

## Troubleshooting

### "No such table" errors
```bash
# Recreate database schema
python -c "from app.db.session import Base, engine; Base.metadata.create_all(bind=engine)"
```

### "Module not found" errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Database locked errors
```bash
# Make sure no other instance is running
# Check Task Manager for python.exe processes
```

## What Gets Transferred?

When setting up on a new machine:

✅ **Automatically Available:**
- Application code
- Database schema (tables, columns, relationships)
- Scripts and documentation

❌ **Not Automatically Available:**
- Your actual data (users, transactions, inventory)
- The fastapi.db file
- Environment-specific configurations

**To transfer data, use one of these methods:**
1. Copy `fastapi.db` file directly
2. Use JSON backups from `backups/` folder
3. Use seed data scripts
