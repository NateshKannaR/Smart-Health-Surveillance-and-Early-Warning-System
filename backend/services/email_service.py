import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json

class EmailService:
    def __init__(self):
        # Gmail SMTP configuration
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "niswan0077@gmail.com"
        self.app_password = "jhhb wkys nesi dacl"  # Your app password
        
    def send_risk_alert(self, recipient_email, prediction_data):
        """Send email alert for high-risk AI predictions"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = f"🚨 HEALTH RISK ALERT - {prediction_data['location']}"
            
            # Create HTML email body
            html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; margin: 20px;">
                <div style="background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <h1 style="margin: 0;">🚨 HEALTH SURVEILLANCE ALERT</h1>
                    <p style="margin: 5px 0 0 0; font-size: 16px;">AI-Powered Risk Detection System</p>
                </div>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #dc3545;">
                    <h2 style="color: #dc3545; margin-top: 0;">⚠️ HIGH RISK PREDICTION DETECTED</h2>
                    
                    <table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
                        <tr style="background: #e9ecef;">
                            <td style="padding: 10px; border: 1px solid #dee2e6; font-weight: bold;">Location:</td>
                            <td style="padding: 10px; border: 1px solid #dee2e6;">{prediction_data['location']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border: 1px solid #dee2e6; font-weight: bold;">Disease:</td>
                            <td style="padding: 10px; border: 1px solid #dee2e6;">{prediction_data['disease'].title()}</td>
                        </tr>
                        <tr style="background: #e9ecef;">
                            <td style="padding: 10px; border: 1px solid #dee2e6; font-weight: bold;">Risk Score:</td>
                            <td style="padding: 10px; border: 1px solid #dee2e6; color: #dc3545; font-weight: bold;">{prediction_data['risk_score']:.1%}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border: 1px solid #dee2e6; font-weight: bold;">Predicted Cases:</td>
                            <td style="padding: 10px; border: 1px solid #dee2e6;">{prediction_data['predicted_cases']}</td>
                        </tr>
                        <tr style="background: #e9ecef;">
                            <td style="padding: 10px; border: 1px solid #dee2e6; font-weight: bold;">Confidence:</td>
                            <td style="padding: 10px; border: 1px solid #dee2e6;">{prediction_data['confidence']:.1%}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border: 1px solid #dee2e6; font-weight: bold;">Alert Time:</td>
                            <td style="padding: 10px; border: 1px solid #dee2e6;">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td>
                        </tr>
                    </table>
                    
                    <h3 style="color: #495057;">🔍 Risk Factors:</h3>
                    <ul style="color: #6c757d;">
            """
            
            # Add risk factors
            factors = json.loads(prediction_data.get('factors', '[]'))
            for factor in factors:
                html_body += f"<li>{factor}</li>"
            
            html_body += f"""
                    </ul>
                    
                    <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h4 style="color: #856404; margin-top: 0;">📋 Recommended Actions:</h4>
                        <ul style="color: #856404; margin-bottom: 0;">
                            <li>Deploy medical teams to {prediction_data['location']}</li>
                            <li>Increase water quality monitoring</li>
                            <li>Distribute health awareness materials</li>
                            <li>Set up temporary health camps</li>
                            <li>Monitor disease progression closely</li>
                        </ul>
                    </div>
                    
                    <div style="background: #d1ecf1; border: 1px solid #bee5eb; padding: 15px; border-radius: 5px;">
                        <p style="color: #0c5460; margin: 0;"><strong>📞 Emergency Contact:</strong> Health Department - 1800-XXX-XXXX</p>
                        <p style="color: #0c5460; margin: 5px 0 0 0;"><strong>🌐 Dashboard:</strong> <a href="http://localhost:8000">Health Surveillance Dashboard</a></p>
                    </div>
                </div>
                
                <div style="text-align: center; color: #6c757d; font-size: 12px; margin-top: 20px;">
                    <p>This alert was generated by the AI-Powered Health Surveillance System</p>
                    <p>Smart Health Surveillance & Early Warning System v2.0</p>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.app_password)
            server.send_message(msg)
            server.quit()
            
            return {
                "status": "success",
                "message": f"Risk alert email sent to {recipient_email}",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error", 
                "message": f"Failed to send email: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def send_test_email(self, recipient_email):
        """Send test email to verify configuration"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = "🧪 Health Surveillance System - Test Email"
            
            body = """
            <html>
            <body style="font-family: Arial, sans-serif; margin: 20px;">
                <h2 style="color: #28a745;">✅ Email Configuration Test Successful!</h2>
                <p>This is a test email from the Health Surveillance System.</p>
                <p><strong>System Status:</strong> ✅ Operational</p>
                <p><strong>Email Service:</strong> ✅ Working</p>
                <p><strong>AI Predictions:</strong> ✅ Ready</p>
                <p><strong>Time:</strong> """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
                <hr>
                <p style="color: #6c757d; font-size: 12px;">Smart Health Surveillance & Early Warning System v2.0</p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.app_password)
            server.send_message(msg)
            server.quit()
            
            return {"status": "success", "message": "Test email sent successfully"}
            
        except Exception as e:
            return {"status": "error", "message": f"Test email failed: {str(e)}"}