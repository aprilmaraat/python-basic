"""
Migration script to convert transaction dates to naive local Philippines Time
This script converts timezone-aware datetimes to naive datetimes representing local time.
"""
import sqlite3
from datetime import datetime
import json
from pathlib import Path

DB_PATH = "fastapi.db"
BACKUP_DIR = Path("backups")

def create_backup():
	"""Create a backup before migration"""
	BACKUP_DIR.mkdir(exist_ok=True)
	timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
	backup_file = BACKUP_DIR / f"backup_before_naive_datetime_{timestamp}.json"
	
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
		"migration_type": "timezone_aware_to_naive_local"
	}
	
	with open(backup_file, "w") as f:
		json.dump(backup_data, f, indent=2)
	
	conn.close()
	print(f"✓ Backup created: {backup_file}")
	return backup_file

def convert_to_naive_local():
	"""Convert all transaction dates to naive local datetime (Philippines time)"""
	conn = sqlite3.connect(DB_PATH)
	cursor = conn.cursor()
	
	# Get all transactions
	cursor.execute("SELECT id, date FROM transactions")
	transactions = cursor.fetchall()
	
	print(f"\n📊 Found {len(transactions)} transactions to convert")
	
	converted_count = 0
	for transaction_id, date_str in transactions:
		try:
			# Parse the existing datetime
			if '+' in date_str or 'Z' in date_str:
				# Timezone-aware format (ISO with timezone)
				dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
				# Already in GMT+8, just remove timezone info
				dt_naive = dt.replace(tzinfo=None)
			elif 'T' in date_str:
				# ISO format without timezone
				dt_naive = datetime.fromisoformat(date_str)
			else:
				# Space separator format
				dt_naive = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f") if '.' in date_str else datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
			
			# Store as naive datetime string (without timezone info)
			new_date_str = dt_naive.strftime("%Y-%m-%d %H:%M:%S.%f")
			
			cursor.execute("UPDATE transactions SET date = ? WHERE id = ?", (new_date_str, transaction_id))
			converted_count += 1
			
			if converted_count % 10 == 0:
				print(f"  Converted {converted_count}/{len(transactions)} transactions...")
		
		except Exception as e:
			print(f"  ⚠ Error converting transaction {transaction_id}: {e}")
			continue
	
	conn.commit()
	conn.close()
	
	print(f"\n✓ Successfully converted {converted_count} transactions to naive local time")
	return converted_count

def verify_conversion():
	"""Verify the conversion was successful"""
	conn = sqlite3.connect(DB_PATH)
	cursor = conn.cursor()
	
	cursor.execute("SELECT id, date FROM transactions ORDER BY id DESC LIMIT 5")
	transactions = cursor.fetchall()
	
	print("\n📋 Sample of converted transactions (naive local time):")
	for tid, date_str in transactions:
		print(f"  ID {tid}: {date_str}")
	
	conn.close()

def main():
	print("=" * 70)
	print("DATETIME MIGRATION: Converting to Naive Local Philippines Time")
	print("=" * 70)
	
	# Step 1: Create backup
	print("\n[1/3] Creating backup...")
	backup_file = create_backup()
	
	# Step 2: Convert dates
	print("\n[2/3] Converting transaction dates to naive local time...")
	converted = convert_to_naive_local()
	
	# Step 3: Verify
	print("\n[3/3] Verifying conversion...")
	verify_conversion()
	
	print("\n" + "=" * 70)
	print("✓ MIGRATION COMPLETED SUCCESSFULLY")
	print(f"  - Backup saved to: {backup_file}")
	print(f"  - Transactions converted: {converted}")
	print("  - All dates are now naive local Philippines time")
	print("=" * 70)

if __name__ == "__main__":
	main()
