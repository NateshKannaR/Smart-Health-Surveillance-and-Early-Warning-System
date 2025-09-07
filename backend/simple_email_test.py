#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.email_service import EmailService

def send_alerts(email):
    service = EmailService()
    
    # Test data
    predictions = [
        {
            'location': 'Guwahati Central',
            'disease': 'diarrhea',
            'risk_score': 0.481,
            'predicted_cases': 5,
            'confidence': 0.57,
            'factors': '["High water contamination", "Monsoon season"]'
        },
        {
            'location': 'Silchar',
            'disease': 'cholera',
            'risk_score': 0.502,
            'predicted_cases': 4,
            'confidence': 0.55,
            'factors': '["Contaminated water sources", "Poor sanitation"]'
        }
    ]
    
    print(f"Sending to: {email}")
    
    # Send test email
    result = service.send_test_email(email)
    print(f"Test email: {result['status']}")
    
    # Send alerts
    for pred in predictions:
        result = service.send_risk_alert(email, pred)
        print(f"{pred['location']}: {result['status']}")
    
    print("Done! Check your email.")

if __name__ == "__main__":
    send_alerts("niswan0077@gmail.com")