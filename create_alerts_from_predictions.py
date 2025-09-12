import sqlite3

def create_alerts():
    conn = sqlite3.connect("health_surveillance.db")
    cursor = conn.cursor()
    
    # Get high-risk predictions
    cursor.execute("SELECT location, disease, risk_score FROM predictions WHERE risk_score > 60 ORDER BY risk_score DESC LIMIT 5")
    predictions = cursor.fetchall()
    
    # Clear old alerts
    cursor.execute("DELETE FROM alerts")
    
    # Create alerts from predictions
    for location, disease, risk_score in predictions:
        if risk_score >= 80:
            severity = "critical"
            message = f"CRITICAL: {disease} outbreak risk {int(risk_score)}% in {location}"
        elif risk_score >= 70:
            severity = "high" 
            message = f"HIGH RISK: {disease} cases increasing in {location} - {int(risk_score)}% risk"
        else:
            severity = "medium"
            message = f"MEDIUM RISK: Monitor {disease} situation in {location} - {int(risk_score)}% risk"
        
        cursor.execute("INSERT INTO alerts (severity, is_active, created_at, location, message) VALUES (?, 1, datetime('now'), ?, ?)",
                      (severity, location, message))
    
    conn.commit()
    
    # Show results
    cursor.execute("SELECT severity, location, message FROM alerts")
    alerts = cursor.fetchall()
    print(f"Created {len(alerts)} alerts:")
    for alert in alerts:
        print(f"  {alert[0].upper()}: {alert[1]} - {alert[2]}")
    
    conn.close()

if __name__ == "__main__":
    create_alerts()