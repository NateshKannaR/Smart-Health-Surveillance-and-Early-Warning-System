import requests
import json

# Test mobile app connection to backend
API_URL = "http://localhost:8000/api"

def test_health_report():
    data = {
        "disease": "diarrhea",
        "severity": "mild", 
        "location": "Test Village"
    }
    
    response = requests.post(f"{API_URL}/health/reports", json=data)
    print(f"Health Report Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_water_source():
    data = {
        "is_safe": False,
        "ph_level": 7.2,
        "turbidity": 5.5,
        "bacterial_count": 150,
        "temperature": 25.0,
        "source_type": "mobile_report"
    }
    
    response = requests.post(f"{API_URL}/water/sources", json=data)
    print(f"Water Source Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_alert():
    data = {
        "severity": "medium",
        "is_active": True
    }
    
    response = requests.post(f"{API_URL}/alerts", json=data)
    print(f"Alert Status: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    print("Testing Mobile to Database Connection...")
    test_health_report()
    test_water_source()
    test_alert()
    print("Test completed!")