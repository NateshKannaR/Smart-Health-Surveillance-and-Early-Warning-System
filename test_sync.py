import sqlite3
import requests
from datetime import datetime

def test_sync():
    # 1. Check database directly
    conn = sqlite3.connect("health_surveillance.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM alerts")
    db_alerts = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM health_reports") 
    db_health = cursor.fetchone()[0]
    
    print(f"Database: {db_alerts} alerts, {db_health} health reports")
    
    # 2. Add test data
    cursor.execute("INSERT INTO alerts (severity, is_active, created_at, location, message) VALUES (?, ?, ?, ?, ?)",
                  ("high", 1, datetime.now(), "TestCity", "Test alert"))
    
    cursor.execute("INSERT INTO health_reports (disease, severity, location, reported_at) VALUES (?, ?, ?, ?)",
                  ("cholera", "severe", "TestCity", datetime.now()))
    
    conn.commit()
    conn.close()
    
    # 3. Test API
    try:
        response = requests.get("http://localhost:8000/api/alerts")
        if response.ok:
            alerts = response.json()
            print(f"API alerts: {len(alerts)}")
        else:
            print(f"API error: {response.status_code}")
    except:
        print("API not accessible")

if __name__ == "__main__":
    test_sync()