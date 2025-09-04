#!/usr/bin/env python3
"""
Database setup script for Health Surveillance System
Creates database tables and initial data
"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database import Base
from backend.models.models import User, HealthReport, WaterQualityReport, Alert, Prediction
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_database():
    """Create database and tables"""
    try:
        # Database configuration - using SQLite for development
        DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./health_surveillance.db")
        
        logger.info(f"Connecting to database: {DATABASE_URL}")
        
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
        # Create session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Create initial users
        create_initial_users(db)
        
        # Create sample data
        create_sample_data(db)
        
        db.close()
        logger.info("Database setup completed successfully")
        
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        sys.exit(1)

def create_initial_users(db):
    """Create initial system users"""
    try:
        # Check if users already exist
        existing_user = db.query(User).first()
        if existing_user:
            logger.info("Users already exist, skipping user creation")
            return
        
        initial_users = [
            {
                "username": "admin",
                "email": "admin@healthsurveillance.gov.in",
                "phone": "+911234567890",
                "role": "admin",
                "location": "Guwahati, Assam",
                "language_preference": "en"
            },
            {
                "username": "health_officer_assam",
                "email": "health.assam@gov.in",
                "phone": "+911234567891",
                "role": "health_official",
                "location": "Guwahati, Assam",
                "language_preference": "as"
            },
            {
                "username": "asha_worker_1",
                "email": "asha1@example.com",
                "phone": "+911234567892",
                "role": "ASHA",
                "location": "Shillong, Meghalaya",
                "language_preference": "en"
            },
            {
                "username": "volunteer_1",
                "email": "volunteer1@example.com",
                "phone": "+911234567893",
                "role": "volunteer",
                "location": "Imphal, Manipur",
                "language_preference": "hi"
            },
            {
                "username": "iot_sensor",
                "email": "iot@healthsurveillance.gov.in",
                "phone": "+911234567894",
                "role": "system",
                "location": "Multiple Locations",
                "language_preference": "en"
            }
        ]
        
        for user_data in initial_users:
            user = User(**user_data)
            db.add(user)
        
        db.commit()
        logger.info(f"Created {len(initial_users)} initial users")
        
    except Exception as e:
        logger.error(f"Failed to create initial users: {e}")
        db.rollback()

def create_sample_data(db):
    """Create sample health and water quality data"""
    try:
        # Sample health reports
        sample_health_reports = [
            {
                "reporter_id": 3,  # ASHA worker
                "patient_age": 5,
                "patient_gender": "female",
                "symptoms": '["fever", "diarrhea", "vomiting"]',
                "location": "Shillong, Meghalaya",
                "severity": "moderate",
                "disease_suspected": "diarrhea"
            },
            {
                "reporter_id": 4,  # Volunteer
                "patient_age": 35,
                "patient_gender": "male",
                "symptoms": '["abdominal_pain", "bloody_stool", "fever"]',
                "location": "Imphal, Manipur",
                "severity": "severe",
                "disease_suspected": "dysentery"
            },
            {
                "reporter_id": 3,
                "patient_age": 28,
                "patient_gender": "female",
                "symptoms": '["nausea", "jaundice", "fatigue"]',
                "location": "Shillong, Meghalaya",
                "severity": "moderate",
                "disease_suspected": "hepatitis_a"
            }
        ]
        
        for report_data in sample_health_reports:
            report = HealthReport(**report_data)
            db.add(report)
        
        # Sample water quality reports
        sample_water_reports = [
            {
                "location": "Guwahati, Assam",
                "ph_level": 6.2,
                "turbidity": 8.5,
                "bacterial_count": 25,
                "chlorine_level": 0.1,
                "temperature": 26.5,
                "tested_by": 5,  # IoT sensor
                "source_type": "river",
                "is_contaminated": True
            },
            {
                "location": "Shillong, Meghalaya",
                "ph_level": 7.2,
                "turbidity": 2.1,
                "bacterial_count": 0,
                "chlorine_level": 0.4,
                "temperature": 22.0,
                "tested_by": 3,
                "source_type": "well",
                "is_contaminated": False
            },
            {
                "location": "Imphal, Manipur",
                "ph_level": 8.8,
                "turbidity": 12.0,
                "bacterial_count": 45,
                "chlorine_level": 0.05,
                "temperature": 28.0,
                "tested_by": 5,
                "source_type": "pond",
                "is_contaminated": True
            }
        ]
        
        for report_data in sample_water_reports:
            report = WaterQualityReport(**report_data)
            db.add(report)
        
        # Sample alerts
        sample_alerts = [
            {
                "alert_type": "outbreak_warning",
                "location": "Shillong, Meghalaya",
                "message": "Increased cases of diarrhea reported in the area. Residents advised to boil water before consumption.",
                "severity": "medium",
                "affected_population": 150
            },
            {
                "alert_type": "water_contamination",
                "location": "Imphal, Manipur",
                "message": "High bacterial contamination detected in local pond. Avoid using water from this source.",
                "severity": "high",
                "affected_population": 300
            }
        ]
        
        for alert_data in sample_alerts:
            alert = Alert(**alert_data)
            db.add(alert)
        
        db.commit()
        logger.info("Sample data created successfully")
        
    except Exception as e:
        logger.error(f"Failed to create sample data: {e}")
        db.rollback()

if __name__ == "__main__":
    create_database()