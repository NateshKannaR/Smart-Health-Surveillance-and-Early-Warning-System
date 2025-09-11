#!/usr/bin/env python3
"""Insert sample data to trigger email alerts"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def insert_trigger_data():
    print("Inserting sample data to trigger email alerts...")
    
    # High-risk health reports (will trigger email)
    health_reports = [
        {
            "disease": "cholera",
            "severity": "severe", 
            "location": "Delhi",
            "patient_age": 5,
            "patient_gender": "male"
        },
        {
            "disease": "cholera",
            "severity": "severe",
            "location": "Delhi", 
            "patient_age": 70,
            "patient_gender": "female"
        },
        {
            "disease": "diarrhea",
            "severity": "severe",
            "location": "Delhi",
            "patient_age": 3,
            "patient_gender": "male"
        },
        {
            "disease": "typhoid",
            "severity": "severe",
            "location": "Delhi",
            "patient_age": 65,
            "patient_gender": "female"
        },
        {
            "disease": "cholera",
            "severity": "moderate",
            "location": "Delhi",
            "patient_age": 45,
            "patient_gender": "male"
        }
    ]
    
    # Contaminated water sources (will trigger email)
    water_sources = [
        {
            "location": "Delhi",
            "is_safe": False,
            "ph_level": 9.5,
            "turbidity": 20.0,
            "bacterial_count": 1500,
            "temperature": 30.0,
            "source_type": "river"
        },
        {
            "location": "Delhi", 
            "is_safe": False,
            "ph_level": 5.2,
            "turbidity": 15.5,
            "bacterial_count": 800,
            "temperature": 28.0,
            "source_type": "well"
        }
    ]
    
    print("\nAdding health reports...")
    for i, report in enumerate(health_reports):
        try:
            response = requests.post(f"{BASE_URL}/api/health/reports", json=report)
            result = response.json()
            print(f"Report {i+1}: {report['disease']} ({report['severity']}) - {result.get('status')}")
            if result.get('alert'):
                print(f"  ALERT: {result['alert']['severity']} risk detected!")
            time.sleep(1)
        except Exception as e:
            print(f"Report {i+1} failed: {e}")
    
    print("\nAdding contaminated water sources...")
    for i, source in enumerate(water_sources):
        try:
            response = requests.post(f"{BASE_URL}/api/water/sources", json=source)
            result = response.json()
            print(f"Source {i+1}: pH {source['ph_level']}, Bacteria {source['bacterial_count']} - {result.get('status')}")
            if result.get('alert'):
                print(f"  ALERT: {result['alert']['severity']} contamination risk!")
            time.sleep(1)
        except Exception as e:
            print(f"Source {i+1} failed: {e}")
    
    print("\nChecking if emails were triggered...")
    try:
        response = requests.get(f"{BASE_URL}/api/ai/predictions")
        predictions = response.json()
        print(f"Total predictions: {len(predictions)}")
        for pred in predictions[:3]:
            risk = pred.get('riskScore', 0)
            if risk > 60:
                print(f"HIGH RISK: {pred['location']} - {pred['disease']} ({risk}% risk)")
                print(f"  Email should be sent automatically!")
    except Exception as e:
        print(f"Prediction check failed: {e}")
    
    print("\nSample data insertion complete!")
    print("Check your email (niswan0077@gmail.com) for alerts!")

if __name__ == "__main__":
    insert_trigger_data()