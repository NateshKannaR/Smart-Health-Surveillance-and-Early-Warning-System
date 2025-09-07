from datetime import datetime
import os

class ConsoleNotificationService:
    def __init__(self):
        self.phone_number = "9345430879"
        
    def send_alert_notification(self, recipients, alert_data):
        """Display alert notification in console"""
        try:
            print("\n" + "="*60)
            print("*** HEALTH SURVEILLANCE ALERT ***")
            print("="*60)
            
            disease = alert_data.get('disease', 'Unknown')
            location = alert_data.get('location', 'Unknown')
            severity = alert_data.get('severity', 'Medium')
            cases = alert_data.get('predicted_cases', 0)
            
            print(f"SMS ALERT TO: {self.phone_number}")
            print(f"DISEASE: {disease.upper()}")
            print(f"LOCATION: {location}")
            print(f"SEVERITY: {severity}")
            print(f"PREDICTED CASES: {cases}")
            print(f"TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            print(f"\nSMS MESSAGE:")
            message = f"HEALTH ALERT: {severity} risk {disease} outbreak in {location}. Predicted cases: {cases}. Immediate action required."
            print(f"'{message}'")
            
            print(f"\nRECIPIENTS ({len(recipients)}):")
            for recipient in recipients:
                priority_icon = "HIGH" if recipient['priority'] == 'high' else "MED"
                print(f"  [{priority_icon}] {recipient['type'].replace('_', ' ').title()}")
            
            print("\nRECOMMENDED ACTIONS:")
            for action in alert_data.get('recommended_actions', []):
                print(f"  • {action}")
            
            print("="*60)
            print("Alert logged successfully!")
            print("Note: SMS requires Rs.100 Fast2SMS transaction to activate")
            print("="*60 + "\n")
            
            return {"status": "displayed", "phone": self.phone_number}
            
        except Exception as e:
            print(f"Console notification error: {e}")
            return {"status": "error", "message": str(e)}

# Global instance
console_service = ConsoleNotificationService()