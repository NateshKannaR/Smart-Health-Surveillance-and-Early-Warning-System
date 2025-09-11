import json
from datetime import datetime
from typing import List, Dict
import sqlite3
import re

class EnhancedSMSService:
    """Enhanced SMS service for data collection and community engagement"""
    
    def __init__(self, db_path: str = "health_surveillance.db"):
        self.db_path = db_path
        self.init_database()
        self.language_templates = self._load_language_templates()
    
    def init_database(self):
        """Initialize SMS-related tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # SMS campaigns table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sms_campaigns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    campaign_name TEXT NOT NULL,
                    message_template TEXT NOT NULL,
                    language TEXT DEFAULT 'en',
                    target_audience TEXT,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # SMS responses table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sms_responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone_number TEXT NOT NULL,
                    message TEXT NOT NULL,
                    parsed_data TEXT,
                    response_type TEXT,
                    processed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # SMS outbound messages table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sms_outbound (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone_numbers TEXT NOT NULL,
                    message TEXT NOT NULL,
                    language TEXT DEFAULT 'en',
                    campaign_id INTEGER,
                    status TEXT DEFAULT 'sent',
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (campaign_id) REFERENCES sms_campaigns (id)
                )
            """)
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"SMS database initialization error: {e}")
    
    def _load_language_templates(self) -> Dict:
        """Load SMS templates in multiple languages"""
        return {
            'health_survey': {
                'en': 'Health Survey: Reply with HEALTH [symptoms] [location] [age]. Example: HEALTH fever diarrhea Guwahati 25',
                'hi': 'स्वास्थ्य सर्वेक्षण: HEALTH [लक्षण] [स्थान] [उम्र] के साथ उत्तर दें। उदाहरण: HEALTH बुखार दस्त गुवाहाटी 25',
                'as': 'স্বাস্থ্য সমীক্ষা: HEALTH [লক্ষণ] [স্থান] [বয়স] দিয়ে উত্তর দিন। উদাহরণ: HEALTH জ্বর ডায়রিয়া গুৱাহাটী 25',
                'bn': 'স্বাস্থ্য সমীক্ষা: HEALTH [লক্ষণ] [স্থান] [বয়স] দিয়ে উত্তর দিন। উদাহরণ: HEALTH জ্বর ডায়রিয়া গুয়াহাটি 25'
            },
            'water_quality': {
                'en': 'Water Quality: Reply with WATER [location] [safe/unsafe] [source]. Example: WATER Village_Well unsafe well',
                'hi': 'पानी की गुणवत्ता: WATER [स्थान] [सुरक्षित/असुरक्षित] [स्रोत] के साथ उत्तर दें। उदाहरण: WATER गांव_कुआं असुरक्षित कुआं',
                'as': 'পানীৰ গুণগত মান: WATER [স্থান] [নিৰাপদ/অনিৰাপদ] [উৎস] দিয়ে উত্তৰ দিব। উদাহৰণ: WATER গাঁও_নলকূপ অনিৰাপদ নলকূপ'
            },
            'symptom_report': {
                'en': 'Symptom Report: Reply with SYMPTOM [fever/diarrhea/vomiting/other] [location]. Example: SYMPTOM fever Shillong',
                'hi': 'लक्षण रिपोर्ट: SYMPTOM [बुखार/दस्त/उल्टी/अन्य] [स्थान] के साथ उत्तर दें। उदाहरण: SYMPTOM बुखार शिलांग',
                'as': 'লক্ষণ প্ৰতিবেদন: SYMPTOM [জ্বৰ/ডায়েৰিয়া/বমি/অন্য] [স্থান] দিয়ে উত্তৰ দিব। উদাহৰণ: SYMPTOM জ্বৰ শ্বিলং'
            },
            'emergency_alert': {
                'en': 'EMERGENCY HEALTH ALERT: {message}. Follow safety guidelines. Reply HELP for assistance.',
                'hi': 'आपातकालीन स्वास्थ्य चेतावनी: {message}। सुरक्षा दिशानिर्देशों का पालन करें। सहायता के लिए HELP का उत्तर दें।',
                'as': 'জৰুৰীকালীন স্বাস্থ্য সতৰ্কবাণী: {message}। সুৰক্ষা নিৰ্দেশনা মানি চলক। সহায়তাৰ বাবে HELP উত্তৰ দিয়ক।'
            }
        }
    
    def send_data_collection_request(self, phone_numbers: List[str], template_type: str, language: str = 'en') -> Dict:
        """Send SMS data collection request"""
        try:
            template = self.language_templates.get(template_type, {}).get(language)
            if not template:
                template = self.language_templates.get(template_type, {}).get('en', 'Data collection request')
            
            # Store outbound message
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO sms_outbound (phone_numbers, message, language)
                VALUES (?, ?, ?)
            """, (json.dumps(phone_numbers), template, language))
            
            conn.commit()
            conn.close()
            
            # Simulate SMS sending (in real implementation, integrate with SMS gateway)
            success_count = len(phone_numbers)
            
            return {
                'status': 'success',
                'success_count': success_count,
                'failed_count': 0,
                'message_id': f'SMS_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
                'template_used': template
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def process_sms_response(self, phone_number: str, message: str) -> Dict:
        """Process incoming SMS response and extract data"""
        try:
            # Store raw response
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Parse message based on format
            parsed_data = self._parse_sms_message(message)
            response_type = parsed_data.get('type', 'unknown')
            
            cursor.execute("""
                INSERT INTO sms_responses 
                (phone_number, message, parsed_data, response_type)
                VALUES (?, ?, ?, ?)
            """, (phone_number, message, json.dumps(parsed_data), response_type))
            
            response_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Process parsed data
            if response_type == 'health':
                self._process_health_response(parsed_data, phone_number)
            elif response_type == 'water':
                self._process_water_response(parsed_data, phone_number)
            elif response_type == 'symptom':
                self._process_symptom_response(parsed_data, phone_number)
            
            return {
                'status': 'success',
                'response_id': response_id,
                'parsed_data': parsed_data,
                'message': 'SMS response processed successfully'
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def _parse_sms_message(self, message: str) -> Dict:
        """Parse SMS message to extract structured data"""
        message = message.upper().strip()
        
        # Health report pattern: HEALTH symptoms location age
        health_pattern = r'HEALTH\s+(.+?)\s+([A-Z_]+)\s+(\d+)'
        health_match = re.search(health_pattern, message)
        if health_match:
            symptoms = health_match.group(1).split()
            return {
                'type': 'health',
                'symptoms': symptoms,
                'location': health_match.group(2).replace('_', ' '),
                'age': int(health_match.group(3))
            }
        
        # Water quality pattern: WATER location status source
        water_pattern = r'WATER\s+([A-Z_]+)\s+(SAFE|UNSAFE)\s+([A-Z_]+)'
        water_match = re.search(water_pattern, message)
        if water_match:
            return {
                'type': 'water',
                'location': water_match.group(1).replace('_', ' '),
                'status': water_match.group(2).lower(),
                'source': water_match.group(3).lower()
            }
        
        # Symptom report pattern: SYMPTOM symptom location
        symptom_pattern = r'SYMPTOM\s+([A-Z]+)\s+([A-Z_]+)'
        symptom_match = re.search(symptom_pattern, message)
        if symptom_match:
            return {
                'type': 'symptom',
                'symptom': symptom_match.group(1).lower(),
                'location': symptom_match.group(2).replace('_', ' ')
            }
        
        # Help request
        if 'HELP' in message:
            return {'type': 'help_request', 'message': message}
        
        return {'type': 'unknown', 'raw_message': message}
    
    def _process_health_response(self, data: Dict, phone_number: str):
        """Process health report from SMS"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Convert symptoms list to primary disease
            symptoms = data.get('symptoms', [])
            primary_disease = 'other'
            if any(s in ['FEVER', 'BUKHAR'] for s in symptoms):
                primary_disease = 'fever'
            elif any(s in ['DIARRHEA', 'DAST', 'LOOSE_MOTION'] for s in symptoms):
                primary_disease = 'diarrhea'
            elif any(s in ['VOMITING', 'ULTI'] for s in symptoms):
                primary_disease = 'vomiting'
            
            cursor.execute("""
                INSERT INTO health_reports 
                (disease, severity, location, reported_at, patient_age, patient_gender)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (primary_disease, 'mild', data.get('location'), datetime.now(), 
                  data.get('age', 25), 'unknown'))
            
            conn.commit()
            conn.close()
            
            # Send confirmation SMS
            self._send_confirmation_sms(phone_number, 'health', data.get('location'))
            
        except Exception as e:
            print(f"Error processing health response: {e}")
    
    def _process_water_response(self, data: Dict, phone_number: str):
        """Process water quality report from SMS"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            is_contaminated = data.get('status') == 'unsafe'
            
            cursor.execute("""
                INSERT INTO water_quality_reports 
                (location, ph_level, turbidity, bacterial_count, temperature, 
                 source_type, is_contaminated, chlorine_level, tested_by, tested_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (data.get('location'), 7.0, 5.0, 100 if is_contaminated else 10, 
                  25.0, data.get('source', 'unknown'), is_contaminated, 0.2, 1, datetime.now()))
            
            conn.commit()
            conn.close()
            
            # Send confirmation SMS
            self._send_confirmation_sms(phone_number, 'water', data.get('location'))
            
        except Exception as e:
            print(f"Error processing water response: {e}")
    
    def _process_symptom_response(self, data: Dict, phone_number: str):
        """Process symptom report from SMS"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO health_reports 
                (disease, severity, location, reported_at, patient_age, patient_gender)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (data.get('symptom'), 'mild', data.get('location'), 
                  datetime.now(), 25, 'unknown'))
            
            conn.commit()
            conn.close()
            
            # Send confirmation SMS
            self._send_confirmation_sms(phone_number, 'symptom', data.get('location'))
            
        except Exception as e:
            print(f"Error processing symptom response: {e}")
    
    def _send_confirmation_sms(self, phone_number: str, report_type: str, location: str):
        """Send confirmation SMS after processing report"""
        confirmations = {
            'health': f'Thank you! Your health report for {location} has been received and will be reviewed by health officials.',
            'water': f'Thank you! Your water quality report for {location} has been received. Authorities will investigate if needed.',
            'symptom': f'Thank you! Your symptom report for {location} has been received. Please seek medical attention if symptoms worsen.'
        }
        
        message = confirmations.get(report_type, 'Thank you! Your report has been received.')
        
        # In real implementation, send actual SMS
        print(f"Confirmation SMS to {phone_number}: {message}")
    
    def get_sms_responses(self, limit: int = 50, processed: bool = None) -> List[Dict]:
        """Get SMS responses with optional processing filter"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if processed is not None:
                cursor.execute("""
                    SELECT id, phone_number, message, parsed_data, response_type, 
                           processed, created_at
                    FROM sms_responses 
                    WHERE processed = ?
                    ORDER BY created_at DESC 
                    LIMIT ?
                """, (processed, limit))
            else:
                cursor.execute("""
                    SELECT id, phone_number, message, parsed_data, response_type, 
                           processed, created_at
                    FROM sms_responses 
                    ORDER BY created_at DESC 
                    LIMIT ?
                """, (limit,))
            
            responses = []
            for row in cursor.fetchall():
                parsed_data = json.loads(row[3]) if row[3] else {}
                responses.append({
                    'id': row[0],
                    'phone': row[1],
                    'message': row[2],
                    'parsed_data': parsed_data,
                    'response_type': row[4],
                    'processed': bool(row[5]),
                    'timestamp': row[6]
                })
            
            conn.close()
            return responses
            
        except Exception as e:
            print(f"Error getting SMS responses: {e}")
            return []
    
    def get_sms_statistics(self) -> Dict:
        """Get SMS service statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total responses
            cursor.execute("SELECT COUNT(*) FROM sms_responses")
            total_responses = cursor.fetchone()[0]
            
            # Responses by type
            cursor.execute("""
                SELECT response_type, COUNT(*) 
                FROM sms_responses 
                GROUP BY response_type
            """)
            type_counts = dict(cursor.fetchall())
            
            # Recent responses (last 24 hours)
            cursor.execute("""
                SELECT COUNT(*) 
                FROM sms_responses 
                WHERE created_at >= datetime('now', '-1 day')
            """)
            recent_responses = cursor.fetchone()[0]
            
            # Processing rate
            cursor.execute("SELECT COUNT(*) FROM sms_responses WHERE processed = 1")
            processed_count = cursor.fetchone()[0]
            processing_rate = (processed_count / total_responses * 100) if total_responses > 0 else 0
            
            conn.close()
            
            return {
                'total_responses': total_responses,
                'type_breakdown': type_counts,
                'recent_responses': recent_responses,
                'processing_rate': round(processing_rate, 2),
                'active_phone_numbers': len(set([r['phone'] for r in self.get_sms_responses(limit=1000)]))
            }
            
        except Exception as e:
            print(f"Error getting SMS statistics: {e}")
            return {}
    
    def send_emergency_alert(self, phone_numbers: List[str], message: str, language: str = 'en') -> Dict:
        """Send emergency health alert via SMS"""
        try:
            template = self.language_templates['emergency_alert'][language]
            formatted_message = template.format(message=message)
            
            # Store outbound emergency message
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO sms_outbound (phone_numbers, message, language)
                VALUES (?, ?, ?)
            """, (json.dumps(phone_numbers), formatted_message, language))
            
            conn.commit()
            conn.close()
            
            return {
                'status': 'success',
                'recipients': len(phone_numbers),
                'message': 'Emergency alert sent successfully'
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}