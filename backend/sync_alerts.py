import sqlite3

def sync_alerts():
    conn = sqlite3.connect("health_surveillance.db")
    cursor = conn.cursor()
    
    # Get high-risk predictions
    cursor.execute("SELECT location, disease, risk_score FROM predictions WHERE risk_score > 50 ORDER BY risk_score DESC")
    predictions = cursor.fetchall()
    
    print(f"Found {len(predictions)} predictions with >50% risk")
    
    # Clear old alerts
    cursor.execute("DELETE FROM alerts")
    
    # Create alerts from predictions
    for location, disease, risk_score in predictions:
        risk_pct = int(risk_score * 100) if risk_score < 1 else int(risk_score)
        
        if risk_pct >= 80:
            severity = "critical"
            message = f"CRITICAL: {disease} outbreak risk {risk_pct}% in {location}"
        elif risk_pct >= 70:
            severity = "high" 
            message = f"HIGH RISK: {disease} cases increasing in {location} - {risk_pct}% risk"
        elif risk_pct >= 60:
            severity = "medium"
            message = f"MEDIUM RISK: Monitor {disease} situation in {location} - {risk_pct}% risk"
        else:
            severity = "low"
            message = f"LOW RISK: {disease} monitoring in {location} - {risk_pct}% risk"
        
        cursor.execute("INSERT INTO alerts (severity, is_active, created_at, location, message) VALUES (?, 1, datetime('now'), ?, ?)",
                      (severity, location, message))
    
    conn.commit()
    
    # Show results
    cursor.execute("SELECT severity, location, message FROM alerts ORDER BY severity DESC")
    alerts = cursor.fetchall()
    print(f"\nCreated {len(alerts)} alerts:")
    for alert in alerts:
        print(f"  {alert[0].upper()}: {alert[1]} - {alert[2]}")
    
    conn.close()

if __name__ == "__main__":
    sync_alerts()