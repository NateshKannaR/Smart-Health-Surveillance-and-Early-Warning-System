import requests
from datetime import datetime

class TelegramService:
    def __init__(self):
        # Create bot: Message @BotFather on Telegram, send /newbot
        self.bot_token = "YOUR_BOT_TOKEN"  # Get from @BotFather
        self.chat_id = "YOUR_CHAT_ID"     # Your Telegram user ID
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        
    def send_alert_telegram(self, recipients, alert_data):
        """Send Telegram alert message"""
        try:
            message = self._create_telegram_message(alert_data, recipients)
            
            url = f"{self.base_url}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                print(f"Telegram alert sent successfully!")
                return {"status": "sent", "response": result}
            else:
                print(f"Telegram failed: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            print(f"Telegram service error: {e}")
            return {"status": "error", "message": str(e)}
    
    def _create_telegram_message(self, alert_data, recipients):
        """Create formatted Telegram message"""
        disease = alert_data.get('disease', 'Unknown')
        location = alert_data.get('location', 'Unknown')
        severity = alert_data.get('severity', 'Medium')
        cases = alert_data.get('predicted_cases', 0)
        
        # Severity emoji
        severity_emoji = "🔴" if severity == "HIGH" else "🟡" if severity == "MEDIUM" else "🟢"
        
        message = f"""
🚨 <b>HEALTH SURVEILLANCE ALERT</b> 🚨

{severity_emoji} <b>SEVERITY:</b> {severity}
🦠 <b>DISEASE:</b> {disease.upper()}
📍 <b>LOCATION:</b> {location}
📊 <b>PREDICTED CASES:</b> {cases}
⏰ <b>TIME:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

<b>RISK FACTORS:</b>
{alert_data.get('risk_factors', 'Multiple indicators')}

<b>RECOMMENDED ACTIONS:</b>
"""
        
        for i, action in enumerate(alert_data.get('recommended_actions', []), 1):
            message += f"{i}. {action}\n"
        
        message += f"\n👥 <b>RECIPIENTS ({len(recipients)}):</b>\n"
        for recipient in recipients:
            priority = "🔴" if recipient['priority'] == 'high' else "🟡"
            message += f"{priority} {recipient['type'].replace('_', ' ').title()}\n"
        
        message += "\n✅ <i>Alert logged in Health Surveillance System</i>"
        
        return message

# Global instance
telegram_service = TelegramService()