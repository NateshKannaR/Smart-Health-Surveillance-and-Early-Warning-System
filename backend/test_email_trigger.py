import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_email_system():
    print("Testing Email Alert System...")
    
    # 1. Test simple email first
    print("\n1. Testing simple email...")
    try:
        response = requests.get(f"{BASE_URL}/api/test-email-simple")
        print(f"Simple email test: {response.json()}")
    except Exception as e:
        print(f"Simple email failed: {e}")
    
    # 2. Force email test
    print("\n2. Testing force email...")
    try:
        response = requests.post(f"{BASE_URL}/api/force-email-test/Delhi")
        print(f"Force email test: {response.json()}")
    except Exception as e:
        print(f"Force email failed: {e}")
    
    # 3. Add severe health reports to trigger ML prediction
    print("\n3. Adding severe health reports...")
    
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
            "disease": "cholera",
            "severity": "severe", 
            "location": "Delhi",
            "patient_age": 65,
            "patient_gender": "female"
        }
    ]
    
    for i, report in enumerate(health_reports):
        try:
            response = requests.post(f"{BASE_URL}/api/health/reports", json=report)
            result = response.json()
            print(f"Health report {i+1}: {result}")
            time.sleep(1)  # Wait between requests
        except Exception as e:
            print(f"Health report {i+1} failed: {e}")
    
    # 4. Add contaminated water source
    print("\n4. Adding contaminated water source...")
    water_source = {
        "location": "Delhi",
        "is_safe": False,
        "ph_level": 9.2,
        "turbidity": 15.5,
        "bacterial_count": 1200,
        "temperature": 28.5,
        "source_type": "river"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/water/sources", json=water_source)
        result = response.json()
        print(f"Water source: {result}")
    except Exception as e:
        print(f"Water source failed: {e}")
    
    # 5. Manual trigger prediction
    print("\n5. Manually triggering prediction...")
    try:
        response = requests.post(f"{BASE_URL}/api/trigger-prediction/Delhi")
        result = response.json()
        print(f"Manual prediction: {result}")
    except Exception as e:
        print(f"Manual prediction failed: {e}")
    
    # 6. Check predictions
    print("\n6. Checking AI predictions...")
    try:
        response = requests.get(f"{BASE_URL}/api/ai/predictions")
        predictions = response.json()
        print(f"Current predictions: {len(predictions)} found")
        for pred in predictions[:2]:  # Show first 2
            print(f"  - {pred['location']}: {pred['disease']} ({pred['riskScore']}% risk)")
    except Exception as e:
        print(f"Predictions check failed: {e}")

if __name__ == "__main__":
    test_email_system()