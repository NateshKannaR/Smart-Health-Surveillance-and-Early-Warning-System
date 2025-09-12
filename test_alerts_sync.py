import requests
import json

def test_alerts_sync():
    """Test alerts API synchronization"""
    base_url = "http://localhost:8000"
    
    try:
        # Test 1: Get current alerts
        print("1. Testing GET /api/alerts...")
        response = requests.get(f"{base_url}/api/alerts")
        print(f"Status: {response.status_code}")
        alerts = response.json()
        print(f"Current alerts: {len(alerts)}")
        for alert in alerts:
            print(f"  - ID {alert['id']}: {alert['severity']} in {alert['location']}")
        
        # Test 2: Create a test alert
        print("\n2. Creating test alert...")
        test_alert = {
            "severity": "high",
            "location": "Test City",
            "message": "Test alert for sync verification"
        }
        response = requests.post(f"{base_url}/api/alerts", json=test_alert)
        print(f"Create status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test 3: Get alerts again to verify sync
        print("\n3. Verifying alert was created...")
        response = requests.get(f"{base_url}/api/alerts")
        new_alerts = response.json()
        print(f"Alerts after creation: {len(new_alerts)}")
        
        # Test 4: Check database status
        print("\n4. Checking database status...")
        try:
            response = requests.get(f"{base_url}/api/database/status")
            if response.status_code == 200:
                db_status = response.json()
                print(f"Database status: {db_status}")
            else:
                print("Database status endpoint not available")
        except:
            print("Could not check database status")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server!")
        print("Make sure the server is running: uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_alerts_sync()