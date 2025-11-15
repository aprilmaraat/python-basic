"""Test script to check if updating a transaction changes its date"""
import sqlite3
from datetime import datetime

# First, check dates before update
print("=== BEFORE UPDATE ===")
conn = sqlite3.connect('fastapi.db')
cursor = conn.cursor()
cursor.execute('SELECT id, title, date FROM transactions ORDER BY id DESC LIMIT 5')
rows = cursor.fetchall()
for r in rows:
    print(f'ID: {r[0]}, Title: {r[1]}, Date: {r[2]}')

# Get the first transaction's info
transaction_id = rows[0][0]
original_date = rows[0][2]
original_title = rows[0][1]

# Now update the transaction (change only the title, not the date)
print(f"\n=== UPDATING TRANSACTION {transaction_id} (Title only) ===")
print(f"Original date: {original_date}")
new_title = original_title + " (UPDATED via SQL)"
cursor.execute('UPDATE transactions SET title = ? WHERE id = ?', (new_title, transaction_id))
conn.commit()
conn.close()

# Check dates after update
print("\n=== AFTER UPDATE ===")
conn = sqlite3.connect('fastapi.db')
cursor = conn.cursor()
cursor.execute('SELECT id, title, date FROM transactions ORDER BY id DESC LIMIT 5')
rows = cursor.fetchall()
for r in rows:
    marker = " <-- CHANGED!" if r[0] == transaction_id and r[2] != original_date else ""
    print(f'ID: {r[0]}, Title: {r[1]}, Date: {r[2]}{marker}')
conn.close()

# Rollback the test change
conn = sqlite3.connect('fastapi.db')
cursor = conn.cursor()
cursor.execute('UPDATE transactions SET title = ? WHERE id = ?', (original_title, transaction_id))
conn.commit()
conn.close()
print(f"\nReverted test changes to transaction {transaction_id}")
