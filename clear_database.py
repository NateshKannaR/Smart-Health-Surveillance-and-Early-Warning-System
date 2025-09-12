import sqlite3
import os

def clear_database():
    """Clear all data from the database tables"""
    db_path = "health_surveillance.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("Clearing database tables...")
        
        # Delete all data from each table
        for table in tables:
            table_name = table[0]
            if table_name != 'sqlite_sequence':  # Skip system table
                cursor.execute(f"DELETE FROM {table_name}")
                print(f"Cleared {table_name}")
        
        # Reset auto-increment counters
        cursor.execute("DELETE FROM sqlite_sequence")
        
        conn.commit()
        conn.close()
        
        print("\nDatabase cleared successfully!")
        print("All health reports, water quality data, predictions, and alerts have been deleted.")
        
    except Exception as e:
        print(f"Error clearing database: {e}")

if __name__ == "__main__":
    clear_database()