#!/usr/bin/env python3
"""
Send Test Results to Email
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.email_service import EmailService
import json

def send_test_results_email(recipient_email):
    """Send comprehensive test results to specified email"""
    
    email_service = EmailService()
    
    # Test data
    test_data = [
        {
            'location': 'Guwahati Central',
            'disease': 'diarrhea',
            'risk_score': 0.481,
            'predicted_cases': 5,
            'confidence': 0.57,
            'factors': '["High water contamination", "Monsoon season", "Population density"]'
        },
        {
            'location': 'Silchar',
            'disease': 'cholera', 
            'risk_score': 0.502,
            'predicted_cases': 4,
            'confidence': 0.55,
            'factors': '["Contaminated water sources", "Poor sanitation", "Recent rainfall"]'
        },
        {
            'location': 'Dibrugarh',
            'disease': 'typhoid',
            'risk_score': 0.471,
            'predicted_cases': 2,
            'confidence': 0.53,
            'factors': '["Food contamination risk", "Water quality issues", "Seasonal patterns"]'
        }
    ]
    
    print(f"Sending test results to: {recipient_email}")
    print("=" * 50)
    
    # Send test email first
    test_result = email_service.send_test_email(recipient_email)
    print(f"Test email: {test_result['status']}")
    
    # Send prediction alerts
    for prediction in test_data:
        try:
            email_result = email_service.send_risk_alert(recipient_email, prediction)
            
            print(f"\n📍 {prediction['location']}:")
            print(f"   Disease: {prediction['disease']}")
            print(f"   Risk: {prediction['risk_score']:.1%}")
            print(f"   Cases: {prediction['predicted_cases']}")
            print(f"   Email: {email_result['status']}")
            
        except Exception as e:
            print(f"Error processing {prediction['location']}: {str(e)}")
    
    print("\n" + "=" * 50)
    print("✅ Test results sent to your email!")
    print("📧 Check your inbox for detailed reports")

if __name__ == "__main__":
    # Get email from user input
    if len(sys.argv) > 1:
        email = sys.argv[1]
    else:
        email = input("Enter your email address: ").strip()
    
    if email and "@" in email:
        send_test_results_email(email)
    else:
        print("❌ Please provide a valid email address")