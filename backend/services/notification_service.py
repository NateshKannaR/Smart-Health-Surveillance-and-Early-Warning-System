import asyncio
from typing import List
from twilio.rest import Client
import os

# SMS service configuration
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")

# Emergency contact numbers by role
EMERGENCY_CONTACTS = {
    "health_official": ["+1234567890", "+1234567891"],
    "district_collector": ["+1234567892"],
    "emergency_response": ["+1234567893", "+1234567894"]
}

async def send_alert_notifications(alert):
    """Send alert notifications via SMS and other channels"""
    
    # Determine recipients based on alert severity and type
    recipients = []
    
    if alert.severity in ["high", "critical"]:
        recipients.extend(EMERGENCY_CONTACTS["health_official"])
        recipients.extend(EMERGENCY_CONTACTS["district_collector"])
    
    if alert.severity == "critical":
        recipients.extend(EMERGENCY_CONTACTS["emergency_response"])
    
    # Format alert message
    message = format_alert_message(alert)
    
    # Send SMS notifications
    if TWILIO_SID and TWILIO_TOKEN:
        await send_sms_notifications(recipients, message)
    
    # Send email notifications (placeholder)
    await send_email_notifications(recipients, alert)
    
    return {"status": "notifications_sent", "recipients": len(recipients)}

def format_alert_message(alert) -> str:
    """Format alert message for SMS"""
    
    severity_emoji = {
        "low": "ℹ️",
        "medium": "⚠️", 
        "high": "🚨",
        "critical": "🆘"
    }
    
    message = f"{severity_emoji.get(alert.severity, '⚠️')} HEALTH ALERT\n"
    message += f"Type: {alert.alert_type.replace('_', ' ').title()}\n"
    message += f"Location: {alert.location}\n"
    message += f"Severity: {alert.severity.upper()}\n"
    message += f"Message: {alert.message}\n"
    
    if alert.affected_population:
        message += f"Affected: {alert.affected_population} people\n"
    
    message += f"Time: {alert.created_at.strftime('%Y-%m-%d %H:%M')}\n"
    message += "Immediate action required!"
    
    return message

async def send_sms_notifications(recipients: List[str], message: str):
    """Send SMS notifications using Twilio"""
    
    if not TWILIO_SID:
        print("SMS service not configured")
        return
    
    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        
        for recipient in recipients:
            client.messages.create(
                body=message,
                from_=TWILIO_PHONE,
                to=recipient
            )
            
        print(f"SMS sent to {len(recipients)} recipients")
        
    except Exception as e:
        print(f"SMS sending failed: {e}")

async def send_email_notifications(recipients: List[str], alert):
    """Send email notifications (placeholder implementation)"""
    
    # This would integrate with email service like SendGrid, AWS SES, etc.
    print(f"Email notifications would be sent to {len(recipients)} recipients")
    
    # Email content would include:
    # - Detailed alert information
    # - Location maps
    # - Recommended actions
    # - Contact information

async def send_community_broadcast(location: str, message: str, language: str = "en"):
    """Send broadcast message to community members in specific location"""
    
    # This would integrate with:
    # - Local radio stations
    # - Community WhatsApp groups
    # - Village announcement systems
    # - Mobile app push notifications
    
    translations = {
        "en": message,
        "hi": f"स्वास्थ्य चेतावनी: {message}",
        "as": f"স্বাস্থ্য সতর্কতা: {message}",
        # Add more tribal language translations
    }
    
    localized_message = translations.get(language, message)
    print(f"Broadcasting to {location} in {language}: {localized_message}")
    
    return {"status": "broadcast_sent", "location": location, "language": language}