import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    endpoints = [
        "/api/alerts",
        "/api/health/reports", 
        "/api/water/sources",
        "/api/ai/predictions"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            print(f"\n{endpoint}:")
            print(f"Status: {response.status_code}")
            if response.ok:
                data = response.json()
                print(f"Data: {json.dumps(data, indent=2)}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Failed to connect: {e}")

if __name__ == "__main__":
    test_api()