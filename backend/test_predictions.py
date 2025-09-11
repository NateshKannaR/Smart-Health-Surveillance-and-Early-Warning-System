import requests
import json

def test_ai_predictions():
    """Test AI predictions with the 6 cases and trigger email alerts"""
    
    base_url = "http://localhost:8000/api"
    
    # Test locations with high-risk cases
    test_locations = [
        "Guwahati Central",  # 3 diarrhea cases - should trigger HIGH RISK alert
        "Silchar",           # 2 cholera cases - should trigger CRITICAL RISK alert  
        "Dibrugarh"          # 1 typhoid case - should trigger MEDIUM RISK alert
    ]
    
    print("Testing AI predictions and email alerts...")
    print("=" * 50)
    
    for location in test_locations:
        try:
            print(f"\nTesting prediction for: {location}")
            
            # Trigger prediction for location
            response = requests.post(f"{base_url}/trigger-prediction/{location}")
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('alert_generated'):
                    print(f"ALERT GENERATED for {location}")
                    print(f"   Disease: {result.get('disease', 'Unknown')}")
                    print(f"   Risk Score: {result.get('risk_score', 0):.1%}")
                    print(f"   Predicted Cases: {result.get('predicted_cases', 0)}")
                    print(f"   Confidence: {result.get('confidence', 0):.1%}")
                    
                    if result.get('email_sent'):
                        print(f"   EMAIL ALERT SENT to niswan0077@gmail.com")
                    else:
                        print(f"   Email alert failed")
                else:
                    print(f"No alert generated for {location}")
            else:
                print(f"API Error: {response.status_code}")
                
        except Exception as e:
            print(f"Error testing {location}: {e}")
    
    print("\n" + "=" * 50)
    print("Test completed! Check your email for risk alerts.")

if __name__ == "__main__":
    test_ai_predictions()