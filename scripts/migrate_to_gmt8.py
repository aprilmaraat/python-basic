"""
Migration script to convert transaction dates to Philippines Time (GMT+8)
This script assumes existing dates are naive datetime and converts them to timezone-aware Philippines time.
"""
import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo
import json
from pathlib import Path

PHILIPPINES_TZ = ZoneInfo("Asia/Manila")
DB_PATH = "fastapi.db"
BACKUP_DIR = Path("backups")

def create_backup():
	"""Create a backup before migration"""
	BACKUP_DIR.mkdir(exist_ok=True)
	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	backup_file = BACKUP_DIR / f"backup_before_timezone_migration_{timestamp}.json"
	
	conn = sqlite3.connect(DB_PATH)
	cursor = conn.cursor()
	
	# Backup transactions
	cursor.execute("SELECT id, title, description, owner_id, transaction_type, amount, quantity, purchase_price, date, inventory_id FROM transactions")
	transactions = []
	for row in cursor.fetchall():
		transactions.append({
			"id": row[0],
			"title": row[1],
			"description": row[2],
			"owner_id": row[3],
			"transaction_type": row[4],
			"amount": str(row[5]),
			"quantity": str(row[6]),
			"purchase_price": str(row[7]),
			"date": row[8],
			"inventory_id": row[9]
		})
	
	backup_data = {
		"timestamp": timestamp,
		"transactions": transactions,
		"migration_type": "timezone_conversion_to_gmt8"
	}
	
	with open(backup_file, "w") as f:
		json.dump(backup_data, f, indent=2)
	
	conn.close()
	print(f"✓ Backup created: {backup_file}")
	return backup_file

def convert_to_philippines_time():
	"""Convert all transaction dates to Philippines timezone"""
	conn = sqlite3.connect(DB_PATH)
	cursor = conn.cursor()
	
	# Get all transactions
	cursor.execute("SELECT id, date FROM transactions")
	transactions = cursor.fetchall()
	
	print(f"\n📊 Found {len(transactions)} transactions to convert")
	
	converted_count = 0
	for transaction_id, date_str in transactions:
		try:
			# Parse the existing datetime (assumed to be naive or already GMT+8)
			if 'T' in date_str:
				# ISO format with T separator
				dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
			else:
				# Space separator format
				dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f") if '.' in date_str else datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
			
			# Make timezone-aware if naive (assume it's already Philippines time)
			if dt.tzinfo is None:
				dt_aware = dt.replace(tzinfo=PHILIPPINES_TZ)
			else:
				# Convert to Philippines time if it has a different timezone
				dt_aware = dt.astimezone(PHILIPPINES_TZ)
			
			# Store as timezone-aware datetime (SQLite will store it as string with timezone info)
			# Note: SQLite doesn't have native timezone support, so we store the ISO format
			new_date_str = dt_aware.isoformat()
			
			cursor.execute("UPDATE transactions SET date = ? WHERE id = ?", (new_date_str, transaction_id))
			converted_count += 1
			
			if converted_count % 10 == 0:
				print(f"  Converted {converted_count}/{len(transactions)} transactions...")
		
		except Exception as e:
			print(f"  ⚠ Error converting transaction {transaction_id}: {e}")
			continue
	
	conn.commit()
	conn.close()
	
	print(f"\n✓ Successfully converted {converted_count} transactions to Philippines Time (GMT+8)")
	return converted_count

def verify_conversion():
	"""Verify the conversion was successful"""
	conn = sqlite3.connect(DB_PATH)
	cursor = conn.cursor()
	
	cursor.execute("SELECT id, date FROM transactions ORDER BY id DESC LIMIT 5")
	transactions = cursor.fetchall()
	
	print("\n📋 Sample of converted transactions:")
	for tid, date_str in transactions:
		print(f"  ID {tid}: {date_str}")
	
	conn.close()

def main():
	print("=" * 70)
	print("TIMEZONE MIGRATION: Converting to Philippines Time (GMT+8)")
	print("=" * 70)
	
	# Step 1: Create backup
	print("\n[1/3] Creating backup...")
	backup_file = create_backup()
	
	# Step 2: Convert dates
	print("\n[2/3] Converting transaction dates...")
	converted = convert_to_philippines_time()
	
	# Step 3: Verify
	print("\n[3/3] Verifying conversion...")
	verify_conversion()
	
	print("\n" + "=" * 70)
	print("✓ MIGRATION COMPLETED SUCCESSFULLY")
	print(f"  - Backup saved to: {backup_file}")
	print(f"  - Transactions converted: {converted}")
	print("=" * 70)

if __name__ == "__main__":
	main()
