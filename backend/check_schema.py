import sqlite3

try:
    conn = sqlite3.connect("health_surveillance.db")
    cursor = conn.cursor()
    
    # Get table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("=== Tables ===")
    for table in tables:
        print(f"- {table[0]}")
    
    # Get schema for each table
    for table in tables:
        table_name = table[0]
        print(f"\n=== {table_name} Schema ===")
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        
        # Get sample data
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  Records: {count}")
        
        if count > 0:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 2")
            rows = cursor.fetchall()
            print("  Sample data:")
            for row in rows:
                print(f"    {row}")
    
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")