#!/usr/bin/env python3
"""
Enhanced Health Surveillance System Setup Script
Sets up all the new features including educational modules, offline functionality,
community volunteer reporting, SMS-based data collection, tribal language support,
and resource allocation dashboard.
"""

import sqlite3
import os
import json
from datetime import datetime

def setup_enhanced_database():
    """Set up enhanced database with all new tables"""
    print("Setting up enhanced database...")
    
    db_path = "health_surveillance.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create enhanced tables
    tables = [
        # Volunteer reports table
        """
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
        """,
        
        # SMS campaigns table
        """
        CREATE TABLE IF NOT EXISTS sms_campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_name TEXT NOT NULL,
            message_template TEXT NOT NULL,
            language TEXT DEFAULT 'en',
            target_audience TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        
        # SMS responses table
        """
        CREATE TABLE IF NOT EXISTS sms_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT NOT NULL,
            message TEXT NOT NULL,
            parsed_data TEXT,
            response_type TEXT,
            processed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        
        # Resource requests table
        """
        CREATE TABLE IF NOT EXISTS resource_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource_type TEXT NOT NULL,
            quantity_requested INTEGER NOT NULL,
            priority TEXT NOT NULL CHECK(priority IN ('low', 'medium', 'high', 'critical')),
            location TEXT NOT NULL,
            requester_name TEXT,
            requester_contact TEXT,
            justification TEXT,
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'rejected', 'fulfilled')),
            requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            approved_at TIMESTAMP,
            fulfilled_at TIMESTAMP
        )
        """,
        
        # Resource allocations table
        """
        CREATE TABLE IF NOT EXISTS resource_allocations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER NOT NULL,
            resource_type TEXT NOT NULL,
            quantity_allocated INTEGER NOT NULL,
            location TEXT NOT NULL,
            allocated_by TEXT,
            allocation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expected_delivery TIMESTAMP,
            actual_delivery TIMESTAMP,
            status TEXT DEFAULT 'allocated' CHECK(status IN ('allocated', 'in_transit', 'delivered', 'cancelled')),
            FOREIGN KEY (request_id) REFERENCES resource_requests (id)
        )
        """,
        
        # Educational content tracking
        """
        CREATE TABLE IF NOT EXISTS education_access_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            language TEXT NOT NULL,
            access_method TEXT DEFAULT 'web',
            location TEXT,
            accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        
        # Offline queue table
        """
        CREATE TABLE IF NOT EXISTS offline_queue (
            id TEXT PRIMARY KEY,
            type TEXT,
            data TEXT,
            timestamp TEXT,
            synced INTEGER DEFAULT 0
        )
        """
    ]
    
    for table_sql in tables:
        try:
            cursor.execute(table_sql)
            print(f"Created table successfully")
        except Exception as e:
            print(f"Error creating table: {e}")
    
    conn.commit()
    conn.close()
    print("Enhanced database setup complete!")

def create_sample_data():
    """Create sample data for testing"""
    print("Creating sample data...")
    
    conn = sqlite3.connect("health_surveillance.db")
    cursor = conn.cursor()
    
    # Sample volunteer reports
    sample_reports = [
        ("John Doe", "Guwahati Central", "health_symptoms", "Multiple cases of diarrhea reported in the community", "en", "verified", "high"),
        ("Mary Smith", "Shillong Market", "water_contamination", "Water source appears contaminated, people getting sick", "en", "pending", "critical"),
        ("Ram Kumar", "Imphal East", "resource_shortage", "Need medical supplies urgently", "hi", "pending", "high"),
        ("Priya Sharma", "Aizawl North", "sanitation_issue", "Poor sanitation conditions in residential area", "en", "verified", "medium")
    ]
    
    for report in sample_reports:
        cursor.execute("""
            INSERT OR IGNORE INTO volunteer_reports 
            (reporter_name, location, report_type, description, language, status, priority)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, report)
    
    # Sample resource requests
    sample_requests = [
        ("Medical Team", 2, "high", "Guwahati", "Dr. Singh", "Outbreak response needed"),
        ("Water Testing Kit", 5, "medium", "Shillong", "Health Officer", "Routine water quality testing"),
        ("Emergency Supplies", 10, "critical", "Imphal", "District Collector", "Emergency response supplies"),
        ("Vehicle", 1, "high", "Aizawl", "Medical Officer", "Patient transport needed")
    ]
    
    for request in sample_requests:
        cursor.execute("""
            INSERT OR IGNORE INTO resource_requests 
            (resource_type, quantity_requested, priority, location, requester_name, justification)
            VALUES (?, ?, ?, ?, ?, ?)
        """, request)
    
    # Sample SMS responses
    sample_sms = [
        ("+91-9876543210", "HEALTH fever diarrhea Guwahati 25", '{"type": "health", "symptoms": ["fever", "diarrhea"], "location": "Guwahati", "age": 25}', "health"),
        ("+91-9876543211", "WATER Village_Well unsafe well", '{"type": "water", "location": "Village Well", "status": "unsafe", "source": "well"}', "water"),
        ("+91-9876543212", "SYMPTOM fever Shillong", '{"type": "symptom", "symptom": "fever", "location": "Shillong"}', "symptom")
    ]
    
    for sms in sample_sms:
        cursor.execute("""
            INSERT OR IGNORE INTO sms_responses 
            (phone_number, message, parsed_data, response_type)
            VALUES (?, ?, ?, ?)
        """, sms)
    
    conn.commit()
    conn.close()
    print("Sample data created!")

def setup_static_directories():
    """Set up static directories for audio and educational content"""
    print("Setting up static directories...")
    
    directories = [
        "static",
        "static/audio",
        "static/images", 
        "static/videos",
        "static/educational_content"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        else:
            print(f"Directory exists: {directory}")

def create_educational_content():
    """Create educational content files"""
    print("Creating educational content...")
    
    educational_content = {
        "water_safety": {
            "en": {
                "title": "Water Safety Guidelines",
                "content": [
                    "Boil water for at least 1 minute before drinking",
                    "Use water purification tablets if boiling is not possible",
                    "Store treated water in clean, covered containers",
                    "Avoid ice unless made from safe water",
                    "Use bottled water from reliable sources"
                ],
                "audio_available": True
            },
            "hi": {
                "title": "पानी की सुरक्षा दिशानिर्देश",
                "content": [
                    "पीने से पहले पानी को कम से कम 1 मिनट तक उबालें",
                    "यदि उबालना संभव नहीं है तो पानी शुद्धीकरण गोलियों का उपयोग करें",
                    "उपचारित पानी को साफ, ढके हुए कंटेनरों में स्टोर करें"
                ],
                "audio_available": True
            },
            "as": {
                "title": "পানীৰ সুৰক্ষা নিৰ্দেশনা",
                "content": [
                    "খোৱাৰ আগতে পানী কমেও ১ মিনিট উতলাওক",
                    "উতলোৱা সম্ভৱ নহ'লে পানী বিশুদ্ধকৰণ টেবলেট ব্যৱহাৰ কৰক"
                ],
                "audio_available": False
            }
        },
        "hygiene_practices": {
            "en": {
                "title": "Personal Hygiene Practices",
                "content": [
                    "Wash hands frequently with soap and clean water",
                    "Use alcohol-based hand sanitizer when soap is unavailable",
                    "Avoid touching face with unwashed hands",
                    "Cover mouth and nose when coughing or sneezing"
                ],
                "audio_available": True
            }
        }
    }
    
    # Save educational content to file
    with open("static/educational_content/content.json", "w", encoding="utf-8") as f:
        json.dump(educational_content, f, ensure_ascii=False, indent=2)
    
    print("Educational content created!")

def create_configuration_file():
    """Create configuration file for the enhanced system"""
    print("Creating configuration file...")
    
    config = {
        "system": {
            "name": "Enhanced Health Surveillance System",
            "version": "2.0.0",
            "features": [
                "Educational Modules",
                "Offline Functionality", 
                "Community Volunteer Reporting",
                "SMS-based Data Collection",
                "Tribal Language Support",
                "Resource Allocation Dashboard"
            ]
        },
        "languages": {
            "supported": ["en", "hi", "as", "bn", "ne", "mni", "garo", "khasi", "mizo"],
            "default": "en"
        },
        "sms": {
            "enabled": True,
            "gateway": "mock",
            "templates": {
                "health_survey": "Health Survey: Reply with HEALTH [symptoms] [location] [age]",
                "water_quality": "Water Quality: Reply with WATER [location] [safe/unsafe] [source]",
                "emergency": "EMERGENCY: {message}. Reply HELP for assistance."
            }
        },
        "resources": {
            "auto_approve_critical": True,
            "default_allocation_timeout": 24,
            "resource_types": [
                "Medical Team",
                "Water Testing Kit", 
                "Emergency Supplies",
                "Vehicle",
                "Medicine"
            ]
        },
        "offline": {
            "max_storage_mb": 50,
            "auto_sync": True,
            "sync_interval_minutes": 30
        }
    }
    
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("Configuration file created!")

def main():
    """Main setup function"""
    print("Enhanced Health Surveillance System Setup")
    print("=" * 50)
    
    try:
        setup_enhanced_database()
        create_sample_data()
        setup_static_directories()
        create_educational_content()
        create_configuration_file()
        
        print("\n" + "=" * 50)
        print("Enhanced system setup completed successfully!")
        print("\nNext steps:")
        print("1. Start the backend server: uvicorn main:app --reload")
        print("2. Access enhanced mobile app: http://localhost:8000/enhanced_features")
        print("3. Test all new features:")
        print("   - Educational modules with tribal language support")
        print("   - Community volunteer reporting")
        print("   - SMS-based data collection")
        print("   - Resource allocation dashboard")
        print("   - Offline functionality")
        print("\nSystem is ready for deployment!")
        
    except Exception as e:
        print(f"Setup failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()