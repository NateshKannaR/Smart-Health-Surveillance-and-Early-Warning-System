#!/usr/bin/env python3
"""Add test alerts for dashboard testing"""

import requests
import json

BASE_URL = "http://localhost:8000"

def add_test_alerts():
    print("Adding test alerts for dashboard...")
    
    alerts = [
        {
            "severity": "critical",
            "location": "Mumbai Central",
            "message": "Cholera outbreak detected - 15+ cases reported in last 24 hours"
        },
        {
            "severity": "high", 
            "location": "Delhi NCR",
            "message": "Water contamination alert - Multiple sources showing high bacterial count"
        },
        {
            "severity": "medium",
            "location": "Bangalore",
            "message": "Increased diarrhea cases - Monitoring situation closely"
        },
        {
            "severity": "low",
            "location": "Chennai",
            "message": "Routine health surveillance - All parameters normal"
        }
    ]
    
    for i, alert in enumerate(alerts):
        try:
            response = requests.post(f"{BASE_URL}/api/alerts", json=alert)
            result = response.json()
            print(f"Alert {i+1}: {alert['severity']} - {alert['location']} - {result.get('status')}")
        except Exception as e:
            print(f"Alert {i+1} failed: {e}")
    
    print("\nTest alerts added successfully!")
    print("Check the dashboard at http://localhost:3000/alerts")

if __name__ == "__main__":
    add_test_alerts()