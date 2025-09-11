import json
import sqlite3
from datetime import datetime
from typing import Dict, List

class OfflineDataService:
    """Offline data synchronization service"""
    
    def __init__(self, db_path: str = "health_surveillance.db"):
        self.db_path = db_path
        self.offline_queue = []
    
    def store_offline_report(self, report_data: Dict, report_type: str) -> Dict:
        """Store report data for offline sync"""
        offline_entry = {
            "id": f"offline_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.offline_queue)}",
            "type": report_type,
            "data": report_data,
            "timestamp": datetime.now().isoformat(),
            "synced": False
        }
        
        self.offline_queue.append(offline_entry)
        
        # Also store in local SQLite for persistence
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS offline_queue (
                    id TEXT PRIMARY KEY,
                    type TEXT,
                    data TEXT,
                    timestamp TEXT,
                    synced INTEGER DEFAULT 0
                )
            """)
            
            cursor.execute("""
                INSERT INTO offline_queue (id, type, data, timestamp, synced)
                VALUES (?, ?, ?, ?, ?)
            """, (offline_entry["id"], report_type, json.dumps(report_data), 
                  offline_entry["timestamp"], 0))
            
            conn.commit()
            conn.close()
            
            return {"status": "stored_offline", "id": offline_entry["id"]}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def sync_offline_data(self) -> Dict:
        """Sync all offline data when connection is available"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get all unsynced offline data
            cursor.execute("SELECT * FROM offline_queue WHERE synced = 0")
            offline_data = cursor.fetchall()
            
            synced_count = 0
            failed_count = 0
            
            for row in offline_data:
                entry_id, report_type, data_json, timestamp, synced = row
                
                try:
                    data = json.loads(data_json)
                    
                    # Process based on report type
                    if report_type == "health_report":
                        self._sync_health_report(data, cursor)
                    elif report_type == "water_report":
                        self._sync_water_report(data, cursor)
                    elif report_type == "alert":
                        self._sync_alert(data, cursor)
                    
                    # Mark as synced
                    cursor.execute("UPDATE offline_queue SET synced = 1 WHERE id = ?", (entry_id,))
                    synced_count += 1
                    
                except Exception as e:
                    failed_count += 1
                    print(f"Failed to sync {entry_id}: {e}")
            
            conn.commit()
            conn.close()
            
            return {
                "status": "sync_complete",
                "synced": synced_count,
                "failed": failed_count
            }
            
        except Exception as e:
            return {"status": "sync_error", "message": str(e)}
    
    def _sync_health_report(self, data: Dict, cursor) -> None:
        """Sync health report to main database"""
        cursor.execute("""
            INSERT INTO health_reports (disease, severity, location, reported_at)
            VALUES (?, ?, ?, ?)
        """, (data.get("disease"), data.get("severity"), 
              data.get("location"), data.get("reported_at", datetime.now())))
    
    def _sync_water_report(self, data: Dict, cursor) -> None:
        """Sync water quality report to main database"""
        cursor.execute("""
            INSERT INTO water_quality_reports 
            (location, ph_level, turbidity, bacterial_count, temperature, 
             source_type, is_contaminated, chlorine_level, tested_by, tested_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (data.get("location"), data.get("ph_level"), data.get("turbidity"),
              data.get("bacterial_count"), data.get("temperature"), 
              data.get("source_type"), data.get("is_contaminated", False),
              data.get("chlorine_level", 0.0), data.get("tested_by", 1), 
              data.get("tested_at", datetime.now())))
    
    def _sync_alert(self, data: Dict, cursor) -> None:
        """Sync alert to main database"""
        cursor.execute("""
            INSERT INTO alerts (severity, is_active, created_at)
            VALUES (?, ?, ?)
        """, (data.get("severity"), 1, data.get("created_at", datetime.now())))
    
    def get_offline_queue_status(self) -> Dict:
        """Get status of offline queue"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM offline_queue WHERE synced = 0")
            pending = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM offline_queue WHERE synced = 1")
            synced = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                "pending_sync": pending,
                "synced_items": synced,
                "total_offline_items": pending + synced
            }
        except:
            return {"pending_sync": 0, "synced_items": 0, "total_offline_items": 0}
    
    def clear_synced_data(self) -> Dict:
        """Clear synced offline data to free up space"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM offline_queue WHERE synced = 1")
            deleted_count = cursor.rowcount
            
            conn.commit()
            conn.close()
            
            return {"status": "cleared", "deleted_items": deleted_count}
        except Exception as e:
            return {"status": "error", "message": str(e)}