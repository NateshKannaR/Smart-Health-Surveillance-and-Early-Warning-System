import sqlite3
from datetime import datetime

def add_test_data():
    conn = sqlite3.connect("health_surveillance.db")
    cursor = conn.cursor()
    
    # Add alerts with proper locations
    cursor.execute("DELETE FROM alerts")
    alerts = [
        ("high", 1, "2024-01-15 10:00:00", "Delhi", "High cholera risk detected"),
        ("medium", 1, "2024-01-15 11:00:00", "Mumbai", "Water contamination reported"),
        ("critical", 1, "2024-01-15 12:00:00", "Bangalore", "Disease outbreak alert")
    ]
    
    cursor.executemany("""
        INSERT INTO alerts (severity, is_active, created_at, location, message)
        VALUES (?, ?, ?, ?, ?)
    """, alerts)
    
    # Add health reports
    cursor.execute("DELETE FROM health_reports")
    health = [
        ("cholera", "severe", "Delhi", "2024-01-15 10:00:00"),
        ("diarrhea", "moderate", "Mumbai", "2024-01-15 11:00:00"),
        ("typhoid", "mild", "Bangalore", "2024-01-15 12:00:00")
    ]
    
    cursor.executemany("""
        INSERT INTO health_reports (disease, severity, location, reported_at)
        VALUES (?, ?, ?, ?)
    """, health)
    
    # Add water reports
    cursor.execute("DELETE FROM water_quality_reports")
    water = [
        ("Delhi", 5.5, 15.0, 50, 28.0, "river", 1, 0.1, 1, "2024-01-15 10:00:00"),
        ("Mumbai", 7.2, 3.0, 5, 26.0, "well", 0, 0.3, 1, "2024-01-15 11:00:00"),
        ("Bangalore", 6.8, 8.0, 25, 24.0, "pond", 1, 0.05, 1, "2024-01-15 12:00:00")
    ]
    
    cursor.executemany("""
        INSERT INTO water_quality_reports 
        (location, ph_level, turbidity, bacterial_count, temperature, source_type, 
         is_contaminated, chlorine_level, tested_by, tested_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, water)
    
    conn.commit()
    
    # Check results
    cursor.execute("SELECT COUNT(*) FROM alerts")
    print(f"Alerts: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM health_reports")
    print(f"Health reports: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM water_quality_reports")
    print(f"Water reports: {cursor.fetchone()[0]}")
    
    conn.close()
    print("Test data added successfully!")

if __name__ == "__main__":
    add_test_data()