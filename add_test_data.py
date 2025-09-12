import sqlite3

def add_test_data():
    conn = sqlite3.connect("health_surveillance.db")
    cursor = conn.cursor()
    
    # Add test alerts
    cursor.execute("DELETE FROM alerts")
    cursor.execute("DELETE FROM health_reports") 
    cursor.execute("DELETE FROM water_quality_reports")
    
    # Add alerts
    cursor.execute("INSERT INTO alerts (severity, is_active, created_at, location, message) VALUES ('high', 1, datetime('now'), 'Delhi', 'High risk cholera outbreak')")
    cursor.execute("INSERT INTO alerts (severity, is_active, created_at, location, message) VALUES ('medium', 1, datetime('now'), 'Mumbai', 'Water contamination detected')")
    
    # Add health reports
    cursor.execute("INSERT INTO health_reports (disease, severity, location, reported_at) VALUES ('cholera', 'severe', 'Delhi', datetime('now'))")
    cursor.execute("INSERT INTO health_reports (disease, severity, location, reported_at) VALUES ('diarrhea', 'moderate', 'Mumbai', datetime('now'))")
    
    # Add water reports
    cursor.execute("INSERT INTO water_quality_reports (location, ph_level, turbidity, bacterial_count, temperature, source_type, is_contaminated, chlorine_level, tested_by, tested_at) VALUES ('Delhi', 5.5, 15, 50, 28, 'river', 1, 0.1, 1, datetime('now'))")
    cursor.execute("INSERT INTO water_quality_reports (location, ph_level, turbidity, bacterial_count, temperature, source_type, is_contaminated, chlorine_level, tested_by, tested_at) VALUES ('Mumbai', 7.2, 3, 5, 26, 'well', 0, 0.3, 1, datetime('now'))")
    
    conn.commit()
    
    # Verify
    cursor.execute("SELECT COUNT(*) FROM alerts")
    alerts = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM health_reports")
    health = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM water_quality_reports")
    water = cursor.fetchone()[0]
    
    print(f"Added: {alerts} alerts, {health} health reports, {water} water reports")
    conn.close()

if __name__ == "__main__":
    add_test_data()