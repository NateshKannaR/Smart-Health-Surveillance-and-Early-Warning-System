#!/usr/bin/env python3
"""Test script to verify alert system functionality"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ml_models.outbreak_prediction import predict_outbreak

def test_alert_system():
    """Test the alert system with sample data"""
    print("Testing Alert System...")
    
    # Sample health reports (high risk scenario)
    health_reports = [
        {'disease': 'cholera', 'severity': 'severe', 'patient_age': 5, 'location': 'Guwahati'},
        {'disease': 'cholera', 'severity': 'severe', 'patient_age': 70, 'location': 'Guwahati'},
        {'disease': 'diarrhea', 'severity': 'moderate', 'patient_age': 3, 'location': 'Guwahati'},
        {'disease': 'cholera', 'severity': 'severe', 'patient_age': 45, 'location': 'Guwahati'},
        {'disease': 'typhoid', 'severity': 'severe', 'patient_age': 65, 'location': 'Guwahati'}
    ]
    
    # Sample water reports (contaminated)
    water_reports = [
        {'location': 'Guwahati', 'ph_level': 5.5, 'turbidity': 15, 'bacterial_count': 500, 'is_contaminated': True},
        {'location': 'Guwahati', 'ph_level': 6.0, 'turbidity': 12, 'bacterial_count': 300, 'is_contaminated': True}
    ]
    
    # Test prediction with alert system
    result = predict_outbreak(health_reports, water_reports, "Guwahati")
    
    print("\n=== PREDICTION RESULT ===")
    print(f"Disease: {result['disease']}")
    print(f"Risk Score: {result['risk_score']:.3f}")
    print(f"Predicted Cases: {result['predicted_cases']}")
    print(f"Risk Factors: {result['factors']}")
    print(f"Alert Generated: {result.get('alert_generated', False)}")
    
    if result.get('alert_generated'):
        alert_data = result.get('alert_data', {})
        print(f"\n=== ALERT DETAILS ===")
        print(f"Severity: {alert_data.get('severity', 'N/A')}")
        print(f"English Message:")
        print(alert_data.get('english_message', 'N/A'))
        print(f"\nHindi Message:")
        try:
            print(alert_data.get('hindi_message', 'N/A'))
        except UnicodeEncodeError:
            print("[Hindi message - encoding issue in terminal]")
        print(f"\nRecipients: {len(result.get('recipients', []))}")
        for recipient in result.get('recipients', []):
            print(f"  - {recipient['type']} ({recipient['priority']} priority)")
    
    return result

if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        import os
        os.system('chcp 65001')  # Set UTF-8 encoding for Windows
    test_alert_system()