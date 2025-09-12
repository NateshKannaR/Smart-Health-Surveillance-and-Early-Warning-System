import sqlite3
from datetime import datetime

def fix_alerts_and_maps():
    """Fix alerts display and maps updating by ensuring data exists"""
    
    # Connect to database
    conn = sqlite3.connect("health_surveillance.db")
    cursor = conn.cursor()
    
    # Check current data
    cursor.execute("SELECT COUNT(*) FROM alerts")
    alert_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM health_reports")
    health_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM water_quality_reports")
    water_count = cursor.fetchone()[0]
    
    print(f"Current data: {alert_count} alerts, {health_count} health reports, {water_count} water reports")
    
    # Add sample data if empty
    if alert_count == 0:
        print("Adding sample alerts...")
        sample_alerts = [
            ("high", 1, datetime.now(), "Delhi", "High cholera risk detected in Delhi area"),
            ("medium", 1, datetime.now(), "Mumbai", "Water contamination reported in Mumbai"),
            ("low", 1, datetime.now(), "Bangalore", "Routine health monitoring alert")
        ]
        
        cursor.executemany("""
            INSERT INTO alerts (severity, is_active, created_at, location, message)
            VALUES (?, ?, ?, ?, ?)
        """, sample_alerts)
        print("✓ Added 3 sample alerts")
    
    if health_count == 0:
        print("Adding sample health reports...")
        sample_health = [
            ("cholera", "severe", "Delhi", datetime.now()),
            ("diarrhea", "moderate", "Mumbai", datetime.now()),
            ("typhoid", "mild", "Bangalore", datetime.now())
        ]
        
        cursor.executemany("""
            INSERT INTO health_reports (disease, severity, location, reported_at)
            VALUES (?, ?, ?, ?)
        """, sample_health)
        print("✓ Added 3 sample health reports")
    
    if water_count == 0:
        print("Adding sample water reports...")
        sample_water = [
            ("Delhi", 5.5, 15.0, 50, 28.0, "river", 1, 0.1, 1, datetime.now()),
            ("Mumbai", 7.2, 3.0, 5, 26.0, "well", 0, 0.3, 1, datetime.now()),
            ("Bangalore", 6.8, 8.0, 25, 24.0, "pond", 1, 0.05, 1, datetime.now())
        ]
        
        cursor.executemany("""
            INSERT INTO water_quality_reports 
            (location, ph_level, turbidity, bacterial_count, temperature, source_type, 
             is_contaminated, chlorine_level, tested_by, tested_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_water)
        print("✓ Added 3 sample water reports")
    
    # Commit changes
    conn.commit()
    
    # Verify data
    cursor.execute("SELECT id, severity, location, message FROM alerts")
    alerts = cursor.fetchall()
    print(f"\nCurrent alerts ({len(alerts)}):")
    for alert in alerts:
        print(f"  - ID {alert[0]}: {alert[1]} in {alert[2]} - {alert[3]}")
    
    cursor.execute("SELECT id, disease, severity, location FROM health_reports")
    health = cursor.fetchall()
    print(f"\nCurrent health reports ({len(health)}):")
    for report in health:
        print(f"  - ID {report[0]}: {report[1]} ({report[2]}) in {report[3]}")
    
    cursor.execute("SELECT id, location, is_contaminated FROM water_quality_reports")
    water = cursor.fetchall()
    print(f"\nCurrent water reports ({len(water)}):")
    for report in water:
        status = "Contaminated" if report[2] else "Safe"
        print(f"  - ID {report[0]}: {report[1]} - {status}")
    
    conn.close()
    print("\n✅ Database updated! Alerts and maps should now display data.")

if __name__ == "__main__":
    fix_alerts_and_maps()