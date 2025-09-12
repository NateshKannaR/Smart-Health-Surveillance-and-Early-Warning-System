import sqlite3

def force_clear_all_data():
    """Force clear all data from database"""
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        
        # Disable foreign key constraints temporarily
        cursor.execute("PRAGMA foreign_keys = OFF")
        
        # Clear all tables with data
        tables_to_clear = [
            "health_reports",
            "water_quality_reports", 
            "water_sources",
            "predictions",
            "alerts",
            "users"
        ]
        
        for table in tables_to_clear:
            try:
                cursor.execute(f"DELETE FROM {table}")
                print(f"Cleared {table}")
            except Exception as e:
                print(f"Table {table} not found or already empty")
        
        # Reset auto-increment sequences
        cursor.execute("UPDATE sqlite_sequence SET seq = 0")
        
        # Re-enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")
        
        conn.commit()
        conn.close()
        
        print("All data cleared successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    force_clear_all_data()