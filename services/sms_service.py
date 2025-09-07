import requests
from datetime import datetime

class SMSService:
    def __init__(self):
        # Using Fast2SMS API (free tier available)
        self.api_key = "ByQGsrtL1ICndb84kXME9NpTiD0aZF3Vu5Jf7SwYmAlK2gehRvf3HJlNTDK2UI9Qdtpk5WRSwPcAbGqu"
        self.base_url = "https://www.fast2sms.com/dev/bulkV2"
        
    def send_alert_sms(self, recipients, alert_data):
        """Send SMS alerts to recipients"""
        try:
            # Create SMS message
            message = self._create_sms_message(alert_data)
            
            # Send to your number for testing
            phone_number = "9345430879"
            
            # Fast2SMS API payload
            payload = {
                'authorization': self.api_key,
                'message': message,
                'numbers': phone_number,
                'route': 'q'  # Quick route
            }
            
            headers = {
                'authorization': self.api_key,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            response = requests.post(self.base_url, data=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                print(f"SMS sent successfully: {result}")
                return {"status": "sent", "response": result}
            else:
                print(f"SMS failed: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            print(f"SMS service error: {e}")
            return {"status": "error", "message": str(e)}
    
    def _create_sms_message(self, alert_data):
        """Create SMS message from alert data"""
        disease = alert_data.get('disease', 'Disease')
        location = alert_data.get('location', 'Location')
        severity = alert_data.get('severity', 'Medium')
        cases = alert_data.get('predicted_cases', 0)
        
        message = f"HEALTH ALERT: {severity} risk {disease} outbreak in {location}. "
        message += f"Predicted cases: {cases}. "
        message += f"Immediate action required. Time: {datetime.now().strftime('%H:%M')}"
        
        # SMS limit is 160 characters
        return message[:160]

# Global instance
sms_service = SMSService()