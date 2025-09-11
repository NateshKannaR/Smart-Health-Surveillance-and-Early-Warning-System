import asyncio
import json
from datetime import datetime
from typing import List, Dict
import aiohttp
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SMSGateway:
    """SMS Gateway for community health reporting and alerts"""
    
    def __init__(self):
        self.api_endpoint = "http://localhost:8000/api"
        self.supported_languages = ['en', 'hi', 'as']
        
        # SMS command patterns
        self.commands = {
            'HEALTH': self.process_health_report,
            'WATER': self.process_water_report,
            'ALERT': self.get_alerts,
            'HELP': self.send_help_message
        }
        
        # Language translations for SMS
        self.translations = {
            'en': {
                'health_report_received': 'Health report received. Thank you for reporting.',
                'water_report_received': 'Water quality report received. Thank you.',
                'invalid_format': 'Invalid format. Send HELP for instructions.',
                'help_message': '''SMS Commands:
HEALTH <age> <gender> <symptoms> <location>
WATER <location> <ph> <turbidity> <bacteria>
ALERT <location>
Example: HEALTH 25 M fever,diarrhea Village_Name'''
            },
            'hi': {
                'health_report_received': 'स्वास्थ्य रिपोर्ट प्राप्त हुई। रिपोर्ट करने के लिए धन्यवाद।',
                'water_report_received': 'पानी की गुणवत्ता रिपोर्ट प्राप्त हुई। धन्यवाद।',
                'invalid_format': 'गलत प्रारूप। निर्देशों के लिए HELP भेजें।',
                'help_message': '''SMS कमांड:
HEALTH <उम्र> <लिंग> <लक्षण> <स्थान>
WATER <स्थान> <ph> <टर्बिडिटी> <बैक्टीरिया>
ALERT <स्थान>
उदाहरण: HEALTH 25 M बुखार,दस्त गांव_नाम'''
            }
        }
    
    async def process_incoming_sms(self, phone_number: str, message: str, language: str = 'en'):
        """Process incoming SMS and route to appropriate handler"""
        try:
            message = message.strip().upper()
            parts = message.split(' ', 1)
            
            if not parts:
                return await self.send_sms(phone_number, self.translations[language]['invalid_format'])
            
            command = parts[0]
            content = parts[1] if len(parts) > 1 else ''
            
            if command in self.commands:
                await self.commands[command](phone_number, content, language)
            else:
                await self.send_sms(phone_number, self.translations[language]['invalid_format'])
                
        except Exception as e:
            logger.error(f"Error processing SMS from {phone_number}: {e}")
            await self.send_sms(phone_number, "Error processing your message. Please try again.")
    
    async def process_health_report(self, phone_number: str, content: str, language: str):
        """Process health report SMS"""
        try:
            # Parse: HEALTH <age> <gender> <symptoms> <location>
            parts = content.split(' ')
            if len(parts) < 4:
                await self.send_sms(phone_number, self.translations[language]['invalid_format'])
                return
            
            age = int(parts[0])
            gender = parts[1].lower()
            symptoms = parts[2].split(',')
            location = ' '.join(parts[3:]).replace('_', ' ')
            
            # Create health report
            report_data = {
                "reporter_id": await self.get_or_create_user(phone_number),
                "patient_age": age,
                "patient_gender": gender,
                "symptoms": symptoms,
                "location": location,
                "severity": "moderate"  # Default severity
            }
            
            # Submit to API
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.api_endpoint}/health/reports", json=report_data) as response:
                    if response.status == 200:
                        await self.send_sms(phone_number, self.translations[language]['health_report_received'])
                        logger.info(f"Health report submitted via SMS from {phone_number}")
                    else:
                        await self.send_sms(phone_number, "Failed to submit report. Please try again.")
                        
        except ValueError:
            await self.send_sms(phone_number, self.translations[language]['invalid_format'])
        except Exception as e:
            logger.error(f"Error processing health report: {e}")
            await self.send_sms(phone_number, "Error processing health report.")
    
    async def process_water_report(self, phone_number: str, content: str, language: str):
        """Process water quality report SMS"""
        try:
            # Parse: WATER <location> <ph> <turbidity> <bacteria>
            parts = content.split(' ')
            if len(parts) < 4:
                await self.send_sms(phone_number, self.translations[language]['invalid_format'])
                return
            
            location = parts[0].replace('_', ' ')
            ph_level = float(parts[1])
            turbidity = float(parts[2])
            bacterial_count = int(parts[3])
            
            # Create water quality report
            report_data = {
                "location": location,
                "ph_level": ph_level,
                "turbidity": turbidity,
                "bacterial_count": bacterial_count,
                "chlorine_level": 0.3,  # Default value
                "temperature": 25.0,    # Default value
                "tested_by": await self.get_or_create_user(phone_number),
                "source_type": "well"   # Default source type
            }
            
            # Submit to API
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.api_endpoint}/water/quality", json=report_data) as response:
                    if response.status == 200:
                        result = await response.json()
                        message = self.translations[language]['water_report_received']
                        if result.get('is_contaminated'):
                            message += " WARNING: Water may be contaminated!"
                        await self.send_sms(phone_number, message)
                        logger.info(f"Water quality report submitted via SMS from {phone_number}")
                    else:
                        await self.send_sms(phone_number, "Failed to submit water report.")
                        
        except ValueError:
            await self.send_sms(phone_number, self.translations[language]['invalid_format'])
        except Exception as e:
            logger.error(f"Error processing water report: {e}")
            await self.send_sms(phone_number, "Error processing water report.")
    
    async def get_alerts(self, phone_number: str, content: str, language: str):
        """Get alerts for a location"""
        try:
            location = content.replace('_', ' ') if content else None
            
            async with aiohttp.ClientSession() as session:
                params = {"location": location} if location else {}
                async with session.get(f"{self.api_endpoint}/alerts", params=params) as response:
                    if response.status == 200:
                        alerts = await response.json()
                        
                        if not alerts:
                            await self.send_sms(phone_number, "No active alerts in your area.")
                            return
                        
                        # Format alerts for SMS
                        alert_messages = []
                        for alert in alerts[:3]:  # Limit to 3 alerts
                            severity_emoji = {"low": "ℹ️", "medium": "⚠️", "high": "🚨", "critical": "🆘"}
                            message = f"{severity_emoji.get(alert['severity'], '⚠️')} {alert['alert_type'].replace('_', ' ').title()}: {alert['message'][:100]}"
                            alert_messages.append(message)
                        
                        full_message = "ACTIVE ALERTS:\n" + "\n\n".join(alert_messages)
                        await self.send_sms(phone_number, full_message)
                    else:
                        await self.send_sms(phone_number, "Failed to get alerts.")
                        
        except Exception as e:
            logger.error(f"Error getting alerts: {e}")
            await self.send_sms(phone_number, "Error getting alerts.")
    
    async def send_help_message(self, phone_number: str, content: str, language: str):
        """Send help message with SMS commands"""
        await self.send_sms(phone_number, self.translations[language]['help_message'])
    
    async def get_or_create_user(self, phone_number: str) -> int:
        """Get or create user for phone number"""
        # This would typically check the database for existing user
        # For now, return a default user ID
        return 1
    
    async def send_sms(self, phone_number: str, message: str):
        """Send SMS to phone number"""
        # This would integrate with actual SMS service (Twilio, AWS SNS, etc.)
        logger.info(f"SMS to {phone_number}: {message}")
        
        # Simulate SMS sending delay
        await asyncio.sleep(0.1)
    
    async def broadcast_alert(self, alert_data: Dict, phone_numbers: List[str], language: str = 'en'):
        """Broadcast alert to multiple phone numbers"""
        severity_emoji = {"low": "ℹ️", "medium": "⚠️", "high": "🚨", "critical": "🆘"}
        
        message = f"{severity_emoji.get(alert_data['severity'], '⚠️')} HEALTH ALERT\n"
        message += f"Type: {alert_data['alert_type'].replace('_', ' ').title()}\n"
        message += f"Location: {alert_data['location']}\n"
        message += f"Message: {alert_data['message']}\n"
        message += "Take immediate precautions!"
        
        # Send to all phone numbers
        tasks = []
        for phone_number in phone_numbers:
            task = asyncio.create_task(self.send_sms(phone_number, message))
            tasks.append(task)
        
        await asyncio.gather(*tasks)
        logger.info(f"Alert broadcast sent to {len(phone_numbers)} recipients")

# SMS Gateway Server
class SMSGatewayServer:
    """SMS Gateway server to handle incoming messages"""
    
    def __init__(self):
        self.gateway = SMSGateway()
        self.community_contacts = {
            # Mock community contact database
            "Guwahati": ["+911234567890", "+911234567891"],
            "Shillong": ["+911234567892", "+911234567893"],
            "Imphal": ["+911234567894", "+911234567895"]
        }
    
    async def handle_webhook(self, request_data: Dict):
        """Handle incoming SMS webhook"""
        phone_number = request_data.get('from')
        message = request_data.get('body', '')
        
        # Detect language (simple heuristic)
        language = 'hi' if any(char in message for char in 'हिन्दी') else 'en'
        
        await self.gateway.process_incoming_sms(phone_number, message, language)
    
    async def send_community_alert(self, location: str, alert_data: Dict):
        """Send alert to community members in specific location"""
        phone_numbers = self.community_contacts.get(location, [])
        if phone_numbers:
            await self.gateway.broadcast_alert(alert_data, phone_numbers)

# Example usage
async def demo_sms_gateway():
    """Demonstrate SMS gateway functionality"""
    gateway = SMSGateway()
    
    # Simulate incoming SMS messages
    test_messages = [
        ("+911234567890", "HEALTH 25 M fever,diarrhea Guwahati", "en"),
        ("+911234567891", "WATER Shillong 6.5 8.2 15", "en"),
        ("+911234567892", "ALERT Imphal", "en"),
        ("+911234567893", "HELP", "en")
    ]
    
    for phone, message, lang in test_messages:
        logger.info(f"Processing SMS: {phone} -> {message}")
        await gateway.process_incoming_sms(phone, message, lang)
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(demo_sms_gateway())