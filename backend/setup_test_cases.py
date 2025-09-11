import sqlite3
import os
from datetime import datetime, timedelta
import random

def clear_and_setup_database():
    """Clear database and add 6 test cases for AI prediction"""
    
    # Remove existing database
    if os.path.exists("health_surveillance.db"):
        os.remove("health_surveillance.db")
        print("Existing database cleared")
    
    # Create new database with tables
    conn = sqlite3.connect("health_surveillance.db")
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
        CREATE TABLE health_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease TEXT NOT NULL,
            severity TEXT NOT NULL,
            location TEXT NOT NULL,
            reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            patient_age INTEGER DEFAULT 25,
            patient_gender TEXT DEFAULT 'unknown'
        )
    """)
    
    cursor.execute("""
        CREATE TABLE water_quality_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            ph_level REAL NOT NULL,
            turbidity REAL NOT NULL,
            bacterial_count INTEGER NOT NULL,
            temperature REAL NOT NULL,
            source_type TEXT NOT NULL,
            is_contaminated BOOLEAN DEFAULT 0,
            chlorine_level REAL DEFAULT 0.2,
            tested_by INTEGER DEFAULT 1,
            tested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            severity TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            location TEXT,
            message TEXT
        )
    """)
    
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
    
    # Add 6 test cases that will trigger AI predictions
    test_cases = [
        # Case 1: Multiple diarrhea cases in Guwahati (high risk)
        {
            'disease': 'diarrhea',
            'severity': 'moderate',
            'location': 'Guwahati Central',
            'age': 35,
            'gender': 'male'
        },
        {
            'disease': 'diarrhea', 
            'severity': 'severe',
            'location': 'Guwahati Central',
            'age': 28,
            'gender': 'female'
        },
        {
            'disease': 'diarrhea',
            'severity': 'moderate', 
            'location': 'Guwahati Central',
            'age': 42,
            'gender': 'male'
        },
        
        # Case 2: Cholera outbreak in Silchar (critical risk)
        {
            'disease': 'cholera',
            'severity': 'severe',
            'location': 'Silchar',
            'age': 30,
            'gender': 'female'
        },
        {
            'disease': 'cholera',
            'severity': 'critical',
            'location': 'Silchar', 
            'age': 55,
            'gender': 'male'
        },
        
        # Case 3: Typhoid case in Dibrugarh (medium risk)
        {
            'disease': 'typhoid',
            'severity': 'moderate',
            'location': 'Dibrugarh',
            'age': 25,
            'gender': 'female'
        }
    ]
    
    # Insert health reports
    for i, case in enumerate(test_cases):
        # Spread cases over last 3 days
        report_time = datetime.now() - timedelta(days=random.randint(0, 3), hours=random.randint(0, 23))
        
        cursor.execute("""
            INSERT INTO health_reports (disease, severity, location, reported_at, patient_age, patient_gender)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (case['disease'], case['severity'], case['location'], report_time, case['age'], case['gender']))
    
    # Add contaminated water sources for high-risk areas
    water_sources = [
        {
            'location': 'Guwahati Central',
            'ph_level': 5.2,  # Acidic - unsafe
            'turbidity': 15.0,  # High turbidity
            'bacterial_count': 1500,  # High bacterial count
            'temperature': 28.5,
            'source_type': 'well',
            'is_contaminated': True
        },
        {
            'location': 'Silchar',
            'ph_level': 4.8,  # Very acidic - unsafe
            'turbidity': 25.0,  # Very high turbidity
            'bacterial_count': 2500,  # Very high bacterial count
            'temperature': 30.0,
            'source_type': 'river',
            'is_contaminated': True
        },
        {
            'location': 'Dibrugarh',
            'ph_level': 7.2,  # Normal pH
            'turbidity': 3.0,  # Low turbidity
            'bacterial_count': 50,  # Low bacterial count
            'temperature': 26.0,
            'source_type': 'tube_well',
            'is_contaminated': False
        }
    ]
    
    for source in water_sources:
        test_time = datetime.now() - timedelta(days=random.randint(0, 2))
        cursor.execute("""
            INSERT INTO water_quality_reports 
            (location, ph_level, turbidity, bacterial_count, temperature, source_type, is_contaminated, tested_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (source['location'], source['ph_level'], source['turbidity'], source['bacterial_count'],
              source['temperature'], source['source_type'], source['is_contaminated'], test_time))
    
    conn.commit()
    conn.close()
    
    print("Database setup complete with 6 test cases")
    print("Test cases added:")
    print("   - 3 diarrhea cases in Guwahati Central (HIGH RISK)")
    print("   - 2 cholera cases in Silchar (CRITICAL RISK)")  
    print("   - 1 typhoid case in Dibrugarh (MEDIUM RISK)")
    print("Water quality data added for all locations")
    print("AI will analyze these cases and send email alerts for high-risk predictions")

if __name__ == "__main__":
    clear_and_setup_database()