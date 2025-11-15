import sqlite3

conn = sqlite3.connect('fastapi.db')
cursor = conn.cursor()
cursor.execute("SELECT sql FROM sqlite_master WHERE type='trigger'")
triggers = cursor.fetchall()
print('Triggers:', triggers if triggers else 'None')
conn.close()
