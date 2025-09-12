import sqlite3
from datetime import datetime

def setup_simple_database():
    """Create simple SQLite database with correct schema"""
    conn = sqlite3.connect("health_surveillance.db")
    cursor = conn.cursor()
    
    # Drop existing tables
    cursor.execute("DROP TABLE IF EXISTS health_reports")
    cursor.execute("DROP TABLE IF EXISTS water_quality_reports") 
    cursor.execute("DROP TABLE IF EXISTS alerts")
    cursor.execute("DROP TABLE IF EXISTS predictions")
    cursor.execute("DROP TABLE IF EXISTS users")
    
    # Create users table
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT,
            phone TEXT,
            role TEXT,
            location TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create health_reports table
    cursor.execute("""
        CREATE TABLE health_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease TEXT NOT NULL,
            severity TEXT NOT NULL,
            location TEXT NOT NULL,
            patient_age INTEGER DEFAULT 25,
            patient_gender TEXT DEFAULT 'unknown',
            reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create water_quality_reports table
    cursor.execute("""
        CREATE TABLE water_quality_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            ph_level REAL DEFAULT 7.0,
            turbidity REAL DEFAULT 0,
            bacterial_count INTEGER DEFAULT 0,
            temperature REAL DEFAULT 25.0,
            source_type TEXT DEFAULT 'unknown',
            is_contaminated BOOLEAN DEFAULT 0,
            chlorine_level REAL DEFAULT 0.2,
            tested_by INTEGER DEFAULT 1,
            tested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create alerts table
    cursor.execute("""
        CREATE TABLE alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            severity TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            location TEXT DEFAULT 'Unknown',
            message TEXT DEFAULT 'Health alert'
        )
    """)
    
    # Create predictions table
    cursor.execute("""
        CREATE TABLE predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            disease TEXT NOT NULL,
            risk_score REAL NOT NULL,
            predicted_cases INTEGER NOT NULL,
            factors TEXT,
            confidence REAL NOT NULL,
            prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print("Database setup complete with clean schema!")

if __name__ == "__main__":
    setup_simple_database()