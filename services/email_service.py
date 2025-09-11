import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class EmailService:
    def __init__(self):
        # Gmail SMTP configuration
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email = "niswan0077@gmail.com"
        self.password = "PASTE_YOUR_16_CHAR_APP_PASSWORD_HERE"  # Replace with actual app password
        
    def send_alert_email(self, recipients, alert_data):
        """Send alert email to recipients"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['Subject'] = f"HEALTH ALERT: {alert_data.get('severity', 'MEDIUM')} Risk - {alert_data.get('disease', 'Disease').upper()}"
            
            # Email body
            body = f"""
HEALTH SURVEILLANCE ALERT

Disease: {alert_data.get('disease', 'Unknown')}
Location: {alert_data.get('location', 'Unknown')}
Severity: {alert_data.get('severity', 'Medium')}
Predicted Cases: {alert_data.get('predicted_cases', 0)}

Risk Factors:
{alert_data.get('risk_factors', 'Multiple indicators')}

Recommended Actions:
{'; '.join(alert_data.get('recommended_actions', ['Immediate attention required']))}

Alert Time: {alert_data.get('timestamp', datetime.now().isoformat())}

This is an automated alert from the Health Surveillance System.
Please take immediate action as recommended.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send to each recipient
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            
            sent_count = 0
            for recipient in recipients:
                try:
                    recipient_email = self._get_recipient_email(recipient)
                    if recipient_email:
                        msg['To'] = recipient_email
                        server.send_message(msg)
                        sent_count += 1
                        print(f"Alert sent to {recipient['type']}: {recipient_email}")
                except Exception as e:
                    print(f"Failed to send to {recipient}: {e}")
            
            server.quit()
            return {"status": "sent", "count": sent_count}
            
        except Exception as e:
            print(f"Email service error: {e}")
            return {"status": "error", "message": str(e)}
    
    def _get_recipient_email(self, recipient):
        """Get email address for recipient type"""
        # For testing, send all alerts to your email
        return "niswan0077@gmail.com"

# Global instance
email_service = EmailService()