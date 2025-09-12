#!/usr/bin/env python3
"""Sample inputs to trigger high-risk predictions and email alerts"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def trigger_high_risk_scenario():
    print("🚨 Triggering HIGH RISK outbreak scenario...")
    
    # SCENARIO: Cholera outbreak in Kolkata during monsoon
    location = "Kolkata"
    
    # 1. Multiple severe health reports (triggers high risk)
    severe_health_reports = [
        {
            "disease": "cholera",
            "severity": "severe",
            "location": location,
            "patient_age": 3,
            "patient_gender": "male"
        },
        {
            "disease": "cholera", 
            "severity": "severe",
            "location": location,
            "patient_age": 75,
            "patient_gender": "female"
        },
        {
            "disease": "cholera",
            "severity": "severe", 
            "location": location,
            "patient_age": 1,
            "patient_gender": "female"
        },
        {
            "disease": "diarrhea",
            "severity": "severe",
            "location": location,
            "patient_age": 68,
            "patient_gender": "male"
        },
        {
            "disease": "cholera",
            "severity": "moderate",
            "location": location,
            "patient_age": 45,
            "patient_gender": "female"
        },
        {
            "disease": "typhoid",
            "severity": "severe",
            "location": location,
            "patient_age": 2,
            "patient_gender": "male"
        }
    ]
    
    # 2. Highly contaminated water sources
    contaminated_water = [
        {
            "location": location,
            "is_safe": False,
            "ph_level": 9.8,  # Very high pH
            "turbidity": 25.0,  # High turbidity
            "bacterial_count": 2500,  # Very high bacteria
            "temperature": 32.0,
            "source_type": "river"
        },
        {
            "location": location,
            "is_safe": False, 
            "ph_level": 4.5,  # Very low pH
            "turbidity": 30.0,
            "bacterial_count": 1800,
            "temperature": 29.0,
            "source_type": "well"
        },
        {
            "location": location,
            "is_safe": False,
            "ph_level": 10.2,  # Extremely high pH
            "turbidity": 35.0,
            "bacterial_count": 3000,  # Extremely high bacteria
            "temperature": 31.0,
            "source_type": "pond"
        }
    ]
    
    print(f"\n📍 Location: {location}")
    print(f"📊 Health Reports: {len(severe_health_reports)} (severe cases)")
    print(f"💧 Water Sources: {len(contaminated_water)} (all contaminated)")
    print(f"🌧️ Season: Monsoon (September - high risk factor)")
    
    print("\n🏥 Adding severe health reports...")
    for i, report in enumerate(severe_health_reports):
        try:
            response = requests.post(f"{BASE_URL}/api/health/reports", json=report)
            result = response.json()
            print(f"  Report {i+1}: {report['disease']} ({report['severity']}) Age {report['patient_age']} - {result.get('status')}")
            if result.get('alert'):
                print(f"    🚨 ALERT: {result['alert']['severity']} risk detected!")
            time.sleep(1)
        except Exception as e:
            print(f"  Report {i+1} failed: {e}")
    
    print("\n💧 Adding contaminated water sources...")
    for i, water in enumerate(contaminated_water):
        try:
            response = requests.post(f"{BASE_URL}/api/water/sources", json=water)
            result = response.json()
            print(f"  Source {i+1}: pH {water['ph_level']}, Bacteria {water['bacterial_count']} - {result.get('status')}")
            if result.get('alert'):
                print(f"    🚨 ALERT: {result['alert']['severity']} contamination!")
            time.sleep(1)
        except Exception as e:
            print(f"  Source {i+1} failed: {e}")
    
    print("\n🤖 Triggering AI prediction...")
    try:
        response = requests.post(f"{BASE_URL}/api/trigger-prediction/{location}")
        result = response.json()
        
        risk_score = result.get('risk_score', 0)
        predicted_cases = result.get('predicted_cases', 0)
        email_sent = result.get('email_sent', False)
        
        print(f"  Disease: {result.get('disease', 'Unknown')}")
        print(f"  Risk Score: {risk_score:.1%}")
        print(f"  Predicted Cases: {predicted_cases}")
        print(f"  Email Alert: {'✅ SENT' if email_sent else '❌ NOT SENT'}")
        
        if email_sent:
            print(f"  📧 Email Result: {result.get('email_result', {}).get('message', 'Unknown')}")
        
        # Expected outcome
        if risk_score > 0.6:
            print(f"\n🎯 SUCCESS: High risk detected ({risk_score:.1%})!")
            print("📧 Email alert should be sent to niswan0077@gmail.com")
        else:
            print(f"\n⚠️ Risk score ({risk_score:.1%}) may not trigger email (threshold: 60%)")
            
    except Exception as e:
        print(f"  Prediction failed: {e}")
    
    print(f"\n✅ High-risk scenario complete for {location}!")
    print("📧 Check email inbox for outbreak alerts!")
    print("🌐 Check dashboard at http://localhost:3000/predictions")

if __name__ == "__main__":
    trigger_high_risk_scenario()