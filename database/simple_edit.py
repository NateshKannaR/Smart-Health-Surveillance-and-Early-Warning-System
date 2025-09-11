import sqlite3

# Connect to database
conn = sqlite3.connect("../health_surveillance.db")
cursor = conn.cursor()

# Check existing tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Existing tables:", tables)

# Check table structure
for table in tables:
    table_name = table[0]
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    print(f"\n{table_name} columns:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")

# View existing data
print("\n=== Current Data ===")
for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
    rows = cursor.fetchall()
    print(f"\n{table_name}:")
    for row in rows:
        print(f"  {row}")

# Add sample data based on existing structure
print("\n=== Adding Sample Data ===")

# Example: Add to health_reports (adjust columns as needed)
try:
    cursor.execute("INSERT INTO health_reports (disease, severity, location) VALUES (?, ?, ?)", 
                   ("Diarrhea", "mild", "Village A"))
    print("Added health report")
except Exception as e:
    print(f"Health report error: {e}")

# Example: Add to water_sources (adjust columns as needed)
try:
    cursor.execute("INSERT INTO water_sources (is_safe, ph_level, source_type) VALUES (?, ?, ?)", 
                   (1, 7.2, "well"))
    print("Added water source")
except Exception as e:
    print(f"Water source error: {e}")

conn.commit()
conn.close()
print("\nDatabase operations complete!")