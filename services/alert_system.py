from datetime import datetime
from typing import Dict, List
import sqlite3

class OutbreakAlertSystem:
    def __init__(self):
        self.risk_thresholds = {
            'high': 0.7,
            'medium': 0.4,
            'low': 0.0
        }
        
    def analyze_and_alert(self, prediction_result: Dict, location: str) -> Dict:
        """Main function to analyze prediction and generate alerts"""
        risk_level = self._determine_risk_level(prediction_result)
        
        if risk_level == 'low':
            return {'alert_needed': False, 'risk_level': 'low'}
            
        alert_data = self._generate_alert(prediction_result, location, risk_level)
        recipients = self._determine_recipients(location, risk_level)
        
        # Store alert in database
        self._store_alert(alert_data, recipients)
        
        return {
            'alert_needed': True,
            'risk_level': risk_level,
            'alert_data': alert_data,
            'recipients': recipients
        }
    
    def _determine_risk_level(self, prediction: Dict) -> str:
        """Determine risk level based on prediction results"""
        risk_score = prediction.get('risk_score', 0)
        predicted_cases = prediction.get('predicted_cases', 0)
        
        if risk_score >= self.risk_thresholds['high'] or predicted_cases > 20:
            return 'high'
        elif risk_score >= self.risk_thresholds['medium'] or predicted_cases > 5:
            return 'medium'
        else:
            return 'low'
    
    def _generate_alert(self, prediction: Dict, location: str, risk_level: str) -> Dict:
        """Generate alert message with all required details"""
        disease = prediction.get('disease', 'waterborne disease')
        predicted_cases = prediction.get('predicted_cases', 0)
        risk_factors = prediction.get('factors', [])
        
        # Generate risk factors text
        factors_text = self._format_risk_factors(risk_factors)
        
        # Generate recommended actions
        actions = self._get_recommended_actions(disease, risk_level, risk_factors)
        
        # Create alert messages
        english_message = self._create_english_message(
            disease, location, risk_level, predicted_cases, factors_text, actions
        )
        
        hindi_message = self._create_hindi_message(
            disease, location, risk_level, predicted_cases, factors_text, actions
        )
        
        return {
            'disease': disease,
            'location': location,
            'severity': risk_level.upper(),
            'predicted_cases': predicted_cases,
            'risk_factors': factors_text,
            'recommended_actions': actions,
            'english_message': english_message,
            'hindi_message': hindi_message,
            'timestamp': datetime.now().isoformat()
        }
    
    def _format_risk_factors(self, factors: List[str]) -> str:
        """Convert risk factors to readable text"""
        factor_map = {
            'high_water_contamination': 'contaminated water sources',
            'severe_cases_present': 'severe cases reported',
            'monsoon_season': 'monsoon season conditions',
            'vulnerable_population_affected': 'vulnerable population at risk'
        }
        
        readable_factors = [factor_map.get(f, f) for f in factors]
        return ', '.join(readable_factors) if readable_factors else 'multiple risk indicators'
    
    def _get_recommended_actions(self, disease: str, risk_level: str, factors: List[str]) -> List[str]:
        """Generate recommended actions based on disease and risk factors"""
        actions = []
        
        if 'high_water_contamination' in factors:
            actions.append('immediate water testing and purification')
        
        if risk_level == 'high':
            actions.extend([
                'deploy medical teams immediately',
                'set up emergency treatment centers',
                'issue public health advisory'
            ])
        elif risk_level == 'medium':
            actions.extend([
                'increase health worker vigilance',
                'conduct community awareness drives',
                'prepare medical supplies'
            ])
        
        if 'monsoon_season' in factors:
            actions.append('intensify sanitation measures')
        
        if 'vulnerable_population_affected' in factors:
            actions.append('prioritize elderly and children care')
        
        return actions[:3]  # Limit to top 3 actions
    
    def _create_english_message(self, disease: str, location: str, risk_level: str, 
                               predicted_cases: int, factors: str, actions: List[str]) -> str:
        """Create English alert message"""
        urgency = "URGENT" if risk_level == 'high' else "ALERT"
        
        message = f"{urgency}: {disease.upper()} OUTBREAK RISK - {risk_level.upper()}\n"
        message += f"Location: {location}\n"
        message += f"Predicted cases: {predicted_cases}\n"
        message += f"Risk factors: {factors}\n"
        message += f"Actions needed: {'; '.join(actions)}\n"
        message += f"Time: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        
        return message
    
    def _create_hindi_message(self, disease: str, location: str, risk_level: str,
                             predicted_cases: int, factors: str, actions: List[str]) -> str:
        """Create Hindi alert message"""
        disease_hindi = {
            'diarrhea': 'दस्त',
            'cholera': 'हैजा', 
            'typhoid': 'टाइफाइड'
        }.get(disease, 'जल जनित रोग')
        
        risk_hindi = {
            'high': 'उच्च',
            'medium': 'मध्यम'
        }.get(risk_level, 'मध्यम')
        
        urgency = "तत्काल" if risk_level == 'high' else "चेतावनी"
        
        message = f"{urgency}: {disease_hindi} फैलने का {risk_hindi} खतरा\n"
        message += f"स्थान: {location}\n"
        message += f"संभावित मामले: {predicted_cases}\n"
        message += f"तुरंत कार्रवाई आवश्यक\n"
        message += f"समय: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        
        return message
    
    def _determine_recipients(self, location: str, risk_level: str) -> List[Dict]:
        """Determine who should receive the alert"""
        recipients = []
        
        # Always include local health workers
        recipients.extend([
            {'type': 'asha_worker', 'location': location, 'priority': 'high'},
            {'type': 'anm_worker', 'location': location, 'priority': 'high'}
        ])
        
        # Add district officials for medium/high risk
        if risk_level in ['medium', 'high']:
            recipients.extend([
                {'type': 'district_health_officer', 'location': location, 'priority': 'high'},
                {'type': 'block_medical_officer', 'location': location, 'priority': 'medium'}
            ])
        
        # Add governance for high risk
        if risk_level == 'high':
            recipients.extend([
                {'type': 'panchayat_secretary', 'location': location, 'priority': 'high'},
                {'type': 'municipal_health_officer', 'location': location, 'priority': 'medium'}
            ])
        
        return recipients
    
    def _store_alert(self, alert_data: Dict, recipients: List[Dict]):
        """Store alert in database and send notifications"""
        try:
            # Store in database
            conn = sqlite3.connect("health_surveillance.db")
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO alerts 
                (alert_type, location, message, severity, is_resolved, affected_population, 
                 created_at, disease, predicted_cases, risk_factors, recommended_actions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                "outbreak_prediction",
                alert_data['location'],
                alert_data['english_message'],
                alert_data['severity'],
                0,
                alert_data['predicted_cases'],
                datetime.now(),
                alert_data['disease'],
                alert_data['predicted_cases'],
                alert_data['risk_factors'],
                '; '.join(alert_data['recommended_actions'])
            ))
            
            conn.commit()
            conn.close()
            
            # Send notifications (Multiple channels)
            try:
                # Try Telegram first (free)
                from services.telegram_service import telegram_service
                telegram_result = telegram_service.send_alert_telegram(recipients, alert_data)
                
                # Try free email
                from services.free_email_service import free_email_service
                email_result = free_email_service.send_alert_email(recipients, alert_data)
                
                # SMS (requires payment)
                from services.sms_service import sms_service
                sms_result = sms_service.send_alert_sms(recipients, alert_data)
                
                # Console fallback
                from services.console_notification import console_service
                console_result = console_service.send_alert_notification(recipients, alert_data)
                
                print(f"Notifications sent - Telegram: {telegram_result.get('status')}, Email: {email_result.get('status')}, SMS: {sms_result.get('status')}")
                
            except Exception as notification_error:
                print(f"Notification failed: {notification_error}")
                
        except Exception as e:
            print(f"Error storing alert: {e}")

# Global instance
alert_system = OutbreakAlertSystem()