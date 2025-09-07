import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class FreeEmailService:
    def __init__(self):
        # Using Gmail with app password (completely free)
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email = "niswan0077@gmail.com"
        self.password = "unul ycul srpz voeu"
        
    def send_alert_email(self, recipients, alert_data):
        """Send free email alert"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = self.email  # Send to yourself
            msg['Subject'] = f"🚨 HEALTH ALERT: {alert_data.get('severity', 'MEDIUM')} - {alert_data.get('disease', 'Disease').upper()}"
            
            # HTML email body
            body = f"""
            <html>
            <body>
            <h2 style="color: red;">🚨 HEALTH SURVEILLANCE ALERT 🚨</h2>
            
            <table border="1" style="border-collapse: collapse; width: 100%;">
            <tr><td><b>Disease</b></td><td>{alert_data.get('disease', 'Unknown')}</td></tr>
            <tr><td><b>Location</b></td><td>{alert_data.get('location', 'Unknown')}</td></tr>
            <tr><td><b>Severity</b></td><td style="color: red;"><b>{alert_data.get('severity', 'Medium')}</b></td></tr>
            <tr><td><b>Predicted Cases</b></td><td>{alert_data.get('predicted_cases', 0)}</td></tr>
            <tr><td><b>Time</b></td><td>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td></tr>
            </table>
            
            <h3>Risk Factors:</h3>
            <p>{alert_data.get('risk_factors', 'Multiple indicators')}</p>
            
            <h3>Recommended Actions:</h3>
            <ul>
            """
            
            for action in alert_data.get('recommended_actions', []):
                body += f"<li>{action}</li>"
            
            body += f"""
            </ul>
            
            <h3>Recipients ({len(recipients)}):</h3>
            <ul>
            """
            
            for recipient in recipients:
                priority_color = "red" if recipient['priority'] == 'high' else "orange"
                body += f'<li style="color: {priority_color};">{recipient["type"].replace("_", " ").title()} ({recipient["priority"]} priority)</li>'
            
            body += """
            </ul>
            
            <p><i>This is an automated alert from the Health Surveillance System.</i></p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            
            print(f"Email alert sent to {self.email}")
            return {"status": "sent", "email": self.email}
            
        except Exception as e:
            print(f"Email service error: {e}")
            return {"status": "error", "message": str(e)}

# Global instance
free_email_service = FreeEmailService()