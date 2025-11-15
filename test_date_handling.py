"""Test to verify date handling in transaction create and update"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"

print("=== Testing Transaction Date Handling ===\n")

# Step 1: Create a transaction without specifying a date (should use current time)
print("1. Creating transaction without date (should default to now)...")
create_data = {
    "title": "Test Transaction - Date Bug Fix",
    "description": "Testing date handling",
    "owner_id": 1,
    "transaction_type": "expense",
    "amount_per_unit": "10.00",
    "quantity": "2.000",
    "purchase_price": "20.00"
    # Note: no 'date' field provided
}
response = requests.post(f"{BASE_URL}/transactions", json=create_data)
if response.status_code == 201:
    transaction = response.json()
    transaction_id = transaction['id']
    original_date = transaction['date']
    print(f"   ✓ Transaction created: ID={transaction_id}, Date={original_date}")
else:
    print(f"   ✗ Failed to create transaction: {response.status_code} - {response.text}")
    exit(1)

# Step 2: Wait a moment then update the transaction (only title, NOT date)
print("\n2. Waiting 2 seconds...")
import time
time.sleep(2)

print("3. Updating transaction title only (date should remain unchanged)...")
update_data = {
    "title": "Test Transaction - UPDATED TITLE"
    # Note: no 'date' field in update - should NOT change the date
}
response = requests.put(f"{BASE_URL}/transactions/{transaction_id}", json=update_data)
if response.status_code == 200:
    updated_transaction = response.json()
    updated_date = updated_transaction['date']
    print(f"   ✓ Transaction updated: ID={transaction_id}, Date={updated_date}")
    
    # Check if date changed
    if original_date == updated_date:
        print(f"   ✓✓ SUCCESS: Date remained unchanged! {original_date}")
    else:
        print(f"   ✗✗ FAILURE: Date changed from {original_date} to {updated_date}")
        print("      This is the bug we're trying to fix!")
else:
    print(f"   ✗ Failed to update transaction: {response.status_code} - {response.text}")

# Step 4: Update the transaction with a specific date
print("\n4. Updating transaction with a specific date...")
specific_date = (datetime.now() - timedelta(days=7)).isoformat()
update_with_date = {
    "date": specific_date
}
response = requests.put(f"{BASE_URL}/transactions/{transaction_id}", json=update_with_date)
if response.status_code == 200:
    updated_transaction = response.json()
    final_date = updated_transaction['date']
    print(f"   ✓ Transaction updated with specific date: {final_date}")
else:
    print(f"   ✗ Failed to update with date: {response.status_code} - {response.text}")

# Step 5: Clean up - delete the test transaction
print("\n5. Cleaning up test transaction...")
response = requests.delete(f"{BASE_URL}/transactions/{transaction_id}")
if response.status_code == 200:
    print(f"   ✓ Test transaction deleted")
else:
    print(f"   ⚠ Warning: Could not delete test transaction {transaction_id}")

print("\n=== Test Complete ===")
