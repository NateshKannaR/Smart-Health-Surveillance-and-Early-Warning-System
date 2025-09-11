#!/usr/bin/env python3
"""Insert fresh data to trigger automatic email alerts"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def trigger_fresh_alerts():
    print("Inserting fresh data to trigger automatic email alerts...")
    
    # Fresh high-risk health reports
    health_reports = [
        {
            "disease": "cholera",
            "severity": "severe", 
            "location": "Mumbai",
            "patient_age": 4,
            "patient_gender": "female"
        },
        {
            "disease": "cholera",
            "severity": "severe",
            "location": "Mumbai", 
            "patient_age": 75,
            "patient_gender": "male"
        },
        {
            "disease": "typhoid",
            "severity": "severe",
            "location": "Mumbai",
            "patient_age": 2,
            "patient_gender": "male"
        }
    ]
    
    # Fresh contaminated water source
    water_source = {
        "location": "Mumbai",
        "is_safe": False,
        "ph_level": 9.8,
        "turbidity": 25.0,
        "bacterial_count": 2000,
        "temperature": 32.0,
        "source_type": "lake"
    }
    
    print("\nAdding fresh health reports...")
    for i, report in enumerate(health_reports):
        try:
            response = requests.post(f"{BASE_URL}/api/health/reports", json=report)
            result = response.json()
            print(f"Report {i+1}: {report['disease']} ({report['severity']}) - {result.get('status')}")
            if result.get('alert'):
                print(f"  ALERT TRIGGERED: {result['alert']['severity']} risk!")
            time.sleep(2)
        except Exception as e:
            print(f"Report {i+1} failed: {e}")
    
    print("\nAdding contaminated water source...")
    try:
        response = requests.post(f"{BASE_URL}/api/water/sources", json=water_source)
        result = response.json()
        print(f"Water source: pH {water_source['ph_level']}, Bacteria {water_source['bacterial_count']} - {result.get('status')}")
        if result.get('alert'):
            print(f"  ALERT TRIGGERED: {result['alert']['severity']} contamination!")
    except Exception as e:
        print(f"Water source failed: {e}")
    
    print("\nFresh data insertion complete!")
    print("Check your email (niswan0077@gmail.com) for automatic alerts!")

if __name__ == "__main__":
    trigger_fresh_alerts()