from typing import Dict, List
import sqlite3
from datetime import datetime
import json

class CommunityVolunteerService:
    """Community volunteer reporting and management service"""
    
    def __init__(self, db_path: str = "health_surveillance.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize community volunteer tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Volunteer reports table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS volunteer_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reporter_name TEXT NOT NULL,
                    location TEXT NOT NULL,
                    report_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    language TEXT DEFAULT 'en',
                    status TEXT DEFAULT 'pending',
                    priority TEXT DEFAULT 'medium',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    verified_at TIMESTAMP,
                    verified_by INTEGER
                )
            """)
            
            # Voice reports table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS voice_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reporter_name TEXT,
                    audio_file_path TEXT,
                    transcription TEXT,
                    language TEXT DEFAULT 'en',
                    processed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Community feedback table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS community_feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    feedback_type TEXT NOT NULL,
                    rating INTEGER CHECK(rating >= 1 AND rating <= 5),
                    comments TEXT,
                    location TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Database initialization error: {e}")
    
    def submit_volunteer_report(self, report_data: Dict) -> Dict:
        """Submit a volunteer report"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Determine priority based on report type
            priority_mapping = {
                'disease_outbreak': 'critical',
                'water_contamination': 'high',
                'health_symptoms': 'medium',
                'sanitation_issue': 'medium',
                'resource_shortage': 'high'
            }
            
            priority = priority_mapping.get(report_data.get('report_type'), 'medium')
            
            cursor.execute("""
                INSERT INTO volunteer_reports 
                (reporter_name, location, report_type, description, language, priority)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                report_data.get('reporter_name'),
                report_data.get('location'),
                report_data.get('report_type'),
                report_data.get('description'),
                report_data.get('language', 'en'),
                priority
            ))
            
            report_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Auto-generate alert for critical reports
            if priority == 'critical':
                self._create_alert_from_report(report_data, report_id)
            
            return {
                'status': 'success',
                'report_id': report_id,
                'priority': priority,
                'message': 'Volunteer report submitted successfully'
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def _create_alert_from_report(self, report_data: Dict, report_id: int):
        """Create an alert from a critical volunteer report"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            alert_message = f"URGENT: {report_data.get('report_type').replace('_', ' ').title()} reported by volunteer {report_data.get('reporter_name')} in {report_data.get('location')}"
            
            cursor.execute("""
                INSERT INTO alerts (severity, is_active, created_at, location, message)
                VALUES (?, ?, ?, ?, ?)
            """, ('critical', 1, datetime.now(), report_data.get('location'), alert_message))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error creating alert from report: {e}")
    
    def get_volunteer_reports(self, status: str = None, limit: int = 50) -> List[Dict]:
        """Get volunteer reports with optional status filter"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if status:
                cursor.execute("""
                    SELECT id, reporter_name, location, report_type, description, 
                           language, status, priority, created_at
                    FROM volunteer_reports 
                    WHERE status = ?
                    ORDER BY created_at DESC 
                    LIMIT ?
                """, (status, limit))
            else:
                cursor.execute("""
                    SELECT id, reporter_name, location, report_type, description, 
                           language, status, priority, created_at
                    FROM volunteer_reports 
                    ORDER BY created_at DESC 
                    LIMIT ?
                """, (limit,))
            
            reports = []
            for row in cursor.fetchall():
                reports.append({
                    'id': row[0],
                    'reporter_name': row[1],
                    'location': row[2],
                    'report_type': row[3],
                    'description': row[4],
                    'language': row[5],
                    'status': row[6],
                    'priority': row[7],
                    'created_at': row[8]
                })
            
            conn.close()
            return reports
            
        except Exception as e:
            print(f"Error getting volunteer reports: {e}")
            return []
    
    def verify_volunteer_report(self, report_id: int, verifier_id: int = 1) -> Dict:
        """Verify a volunteer report"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE volunteer_reports 
                SET status = 'verified', verified_at = ?, verified_by = ?
                WHERE id = ?
            """, (datetime.now(), verifier_id, report_id))
            
            if cursor.rowcount > 0:
                conn.commit()
                conn.close()
                return {'status': 'success', 'message': 'Report verified successfully'}
            else:
                conn.close()
                return {'status': 'error', 'message': 'Report not found'}
                
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def submit_community_feedback(self, feedback_data: Dict) -> Dict:
        """Submit community feedback"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO community_feedback 
                (feedback_type, rating, comments, location)
                VALUES (?, ?, ?, ?)
            """, (
                feedback_data.get('feedback_type'),
                feedback_data.get('rating'),
                feedback_data.get('comments'),
                feedback_data.get('location')
            ))
            
            conn.commit()
            conn.close()
            
            return {'status': 'success', 'message': 'Feedback submitted successfully'}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def get_community_stats(self) -> Dict:
        """Get community engagement statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total volunteer reports
            cursor.execute("SELECT COUNT(*) FROM volunteer_reports")
            total_reports = cursor.fetchone()[0]
            
            # Reports by status
            cursor.execute("""
                SELECT status, COUNT(*) 
                FROM volunteer_reports 
                GROUP BY status
            """)
            status_counts = dict(cursor.fetchall())
            
            # Reports by priority
            cursor.execute("""
                SELECT priority, COUNT(*) 
                FROM volunteer_reports 
                GROUP BY priority
            """)
            priority_counts = dict(cursor.fetchall())
            
            # Recent activity (last 7 days)
            cursor.execute("""
                SELECT COUNT(*) 
                FROM volunteer_reports 
                WHERE created_at >= datetime('now', '-7 days')
            """)
            recent_reports = cursor.fetchone()[0]
            
            # Average feedback rating
            cursor.execute("SELECT AVG(rating) FROM community_feedback")
            avg_rating = cursor.fetchone()[0] or 0
            
            conn.close()
            
            return {
                'total_reports': total_reports,
                'status_breakdown': status_counts,
                'priority_breakdown': priority_counts,
                'recent_reports': recent_reports,
                'average_rating': round(avg_rating, 2),
                'active_volunteers': len(set([r['reporter_name'] for r in self.get_volunteer_reports(limit=100)]))
            }
            
        except Exception as e:
            print(f"Error getting community stats: {e}")
            return {}
    
    def get_volunteer_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get top volunteers by number of reports"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT reporter_name, COUNT(*) as report_count,
                       MAX(created_at) as last_report
                FROM volunteer_reports 
                GROUP BY reporter_name 
                ORDER BY report_count DESC 
                LIMIT ?
            """, (limit,))
            
            leaderboard = []
            for row in cursor.fetchall():
                leaderboard.append({
                    'volunteer_name': row[0],
                    'report_count': row[1],
                    'last_report': row[2]
                })
            
            conn.close()
            return leaderboard
            
        except Exception as e:
            print(f"Error getting volunteer leaderboard: {e}")
            return []