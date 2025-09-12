#!/usr/bin/env python3
"""Clear old predictions from database"""

import sqlite3
from datetime import datetime, timedelta

def clear_old_predictions():
    """Clear predictions older than 1 hour"""
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        
        # Delete predictions older than 1 hour
        one_hour_ago = datetime.now() - timedelta(hours=1)
        cursor.execute("DELETE FROM predictions WHERE prediction_date < ?", (one_hour_ago,))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        print(f"Cleared {deleted_count} old predictions")
        return {"status": "success", "deleted": deleted_count}
    except Exception as e:
        print(f"Error clearing predictions: {e}")
        return {"status": "error", "message": str(e)}

def clear_all_predictions():
    """Clear all predictions"""
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM predictions")
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        print(f"Cleared all {deleted_count} predictions")
        return {"status": "success", "deleted": deleted_count}
    except Exception as e:
        print(f"Error clearing all predictions: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "all":
        clear_all_predictions()
    else:
        clear_old_predictions()