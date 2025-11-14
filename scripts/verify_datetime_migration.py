"""
Verify datetime migration by checking database schema and querying data
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import inspect, text
from app.db.session import engine, SessionLocal
from datetime import datetime

print("=" * 70)
print("DATETIME MIGRATION VERIFICATION")
print("=" * 70)
print()

# Check schema
print("Step 1: Checking database schema...")
print("-" * 70)
inspector = inspect(engine)
columns = inspector.get_columns('transactions')
date_column = next((c for c in columns if c['name'] == 'date'), None)

if date_column:
    print(f"✓ Date column found")
    print(f"  Type: {date_column['type']}")
    print(f"  Nullable: {date_column['nullable']}")
else:
    print("✗ Date column not found")
    sys.exit(1)

print()

# Check data
print("Step 2: Checking transaction data...")
print("-" * 70)

with engine.connect() as conn:
    result = conn.execute(text("SELECT id, title, date FROM transactions LIMIT 5"))
    rows = result.fetchall()
    
    if rows:
        print(f"✓ Found {len(rows)} transactions")
        print()
        print("Sample transactions:")
        for row in rows:
            print(f"  ID {row[0]}: {row[1]}")
            print(f"    Date: {row[2]} (type: {type(row[2]).__name__})")
            if isinstance(row[2], str):
                # Parse the datetime string
                try:
                    dt = datetime.fromisoformat(row[2].replace(' ', 'T'))
                    print(f"    Parsed: {dt}")
                except:
                    print(f"    Could not parse datetime")
            print()
    else:
        print("No transactions found in database")

print("=" * 70)
print("VERIFICATION COMPLETE!")
print("=" * 70)
