import sqlite3
import os

# Check which database files exist
print("=== Database Files ===")
files = ["health_surveillance.db", "../health_surveillance.db", "backend/health_surveillance.db"]
for f in files:
    if os.path.exists(f):
        print(f"Found: {f}")
        size = os.path.getsize(f)
        print(f"  Size: {size} bytes")
    else:
        print(f"Missing: {f}")

print("\n=== Testing Database Connection ===")
try:
    conn = sqlite3.connect("health_surveillance.db")
    cursor = conn.cursor()
    
    # Test health_reports
    cursor.execute("SELECT COUNT(*) FROM health_reports")
    health_count = cursor.fetchone()[0]
    print(f"Health reports count: {health_count}")
    
    if health_count > 0:
        cursor.execute("SELECT id, disease_suspected, severity, location FROM health_reports LIMIT 3")
        health_data = cursor.fetchall()
        print("Sample health reports:")
        for row in health_data:
            print(f"  ID: {row[0]}, Disease: {row[1]}, Severity: {row[2]}, Location: {row[3]}")
    
    # Test alerts
    cursor.execute("SELECT COUNT(*) FROM alerts")
    alert_count = cursor.fetchone()[0]
    print(f"\nAlerts count: {alert_count}")
    
    if alert_count > 0:
        cursor.execute("SELECT id, severity, message, is_resolved FROM alerts LIMIT 3")
        alert_data = cursor.fetchall()
        print("Sample alerts:")
        for row in alert_data:
            print(f"  ID: {row[0]}, Severity: {row[1]}, Message: {row[2][:50]}..., Resolved: {row[3]}")
    
    conn.close()
    print("\nDatabase connection successful!")
    
except Exception as e:
    print(f"Database error: {e}")