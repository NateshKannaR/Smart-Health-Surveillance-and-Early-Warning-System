import sqlite3

conn = sqlite3.connect("health_surveillance.db")
cursor = conn.cursor()

print("=== Health Reports Table Structure ===")
cursor.execute("PRAGMA table_info(health_reports)")
columns = cursor.fetchall()
for col in columns:
    print(f"  {col[1]} ({col[2]})")

print("\n=== Sample Health Report ===")
cursor.execute("SELECT * FROM health_reports LIMIT 1")
sample = cursor.fetchone()
if sample:
    print("Sample row:", sample)

print("\n=== Alerts Table Structure ===")
cursor.execute("PRAGMA table_info(alerts)")
columns = cursor.fetchall()
for col in columns:
    print(f"  {col[1]} ({col[2]})")

print("\n=== Sample Alert ===")
cursor.execute("SELECT * FROM alerts LIMIT 1")
sample = cursor.fetchone()
if sample:
    print("Sample row:", sample)

conn.close()