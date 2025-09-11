import json
from datetime import datetime
from typing import List, Dict

class SMSService:
    """SMS Gateway Service for community alerts"""
    
    def __init__(self):
        self.sent_messages = []
    
    def send_alert(self, phone_numbers: List[str], message: str, language: str = "en") -> Dict:
        """Send SMS alert to multiple recipients"""
        
        # Translate message based on language
        translated_message = self.translate_message(message, language)
        
        success_count = 0
        failed_numbers = []
        
        for phone in phone_numbers:
            try:
                # Simulate SMS sending
                self.sent_messages.append({
                    "phone": phone,
                    "message": translated_message,
                    "timestamp": datetime.now(),
                    "status": "sent"
                })
                success_count += 1
            except Exception as e:
                failed_numbers.append(phone)
        
        return {
            "success_count": success_count,
            "failed_count": len(failed_numbers),
            "failed_numbers": failed_numbers,
            "message_id": f"SMS_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        }
    
    def translate_message(self, message: str, language: str) -> str:
        """Translate message to local language"""
        translations = {
            "en": message,
            "hi": f"स्वास्थ्य चेतावनी: {message}",
            "as": f"স্বাস্থ্য সতর্কতা: {message}",
            "bn": f"স্বাস্থ্য সতর্কতা: {message}",
            "ne": f"स्वास्थ्य चेतावनी: {message}"
        }
        return translations.get(language, message)
    
    def send_community_report_request(self, phone_numbers: List[str], language: str = "en") -> Dict:
        """Send SMS requesting community health reports"""
        
        messages = {
            "en": "Health Alert: Report any symptoms of diarrhea, fever, or vomiting in your area. Reply with location and symptoms.",
            "hi": "स्वास्थ्य अलर्ट: अपने क्षेत्र में दस्त, बुखार या उल्टी के लक्षणों की रिपोर्ट करें।",
            "as": "স্বাস্থ্য সতর্কতা: আপনার এলাকায় ডায়রিয়া, জ্বর বা বমির লক্ষণ রিপোর্ট করুন।"
        }
        
        message = messages.get(language, messages["en"])
        return self.send_alert(phone_numbers, message, language)