# Enhanced API endpoints for Smart Health Surveillance System
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from datetime import datetime
from services.sms_service import SMSService
from services.iot_service import IoTWaterSensorService
from services.education_service import HealthEducationService
from services.offline_service import OfflineDataService
from services.ml_prediction import predict_outbreak

router = APIRouter()

# Initialize services
sms_service = SMSService()
iot_service = IoTWaterSensorService()
education_service = HealthEducationService()
offline_service = OfflineDataService()

# Pydantic models
class SMSAlertRequest(BaseModel):
    phone_numbers: List[str]
    message: str
    language: Optional[str] = "en"

class CommunityReportRequest(BaseModel):
    reporter_name: str
    location: str
    symptoms: List[str]
    patient_count: Optional[int] = 1
    language: Optional[str] = "en"

class OfflineReportRequest(BaseModel):
    report_type: str
    data: dict

# SMS and Community Engagement APIs
@router.post("/sms/send-alert")
async def send_sms_alert(request: SMSAlertRequest):
    """Send SMS alerts to community members"""
    result = sms_service.send_alert(request.phone_numbers, request.message, request.language)
    return result

@router.post("/community/report")
async def submit_community_report(request: CommunityReportRequest):
    """Submit health report from community member via SMS or voice"""
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        
        symptoms_str = ", ".join(request.symptoms)
        cursor.execute("""
            INSERT INTO health_reports (disease, severity, location, reported_at)
            VALUES (?, ?, ?, ?)
        """, (symptoms_str, "community_report", request.location, datetime.now()))
        
        conn.commit()
        conn.close()
        
        return {"status": "success", "message": "Community report submitted successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# IoT Water Sensor APIs
@router.post("/iot/sensors/register")
async def register_water_sensor(sensor_id: str, location: str):
    """Register new IoT water quality sensor"""
    result = iot_service.register_sensor(sensor_id, location)
    return result

@router.get("/iot/sensors/{sensor_id}/reading")
async def get_sensor_reading(sensor_id: str):
    """Get current reading from IoT water sensor"""
    reading = iot_service.get_sensor_reading(sensor_id)
    
    if "error" not in reading:
        try:
            conn = sqlite3.connect("health_surveillance.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO water_quality_reports 
                (location, ph_level, turbidity, bacterial_count, temperature, 
                 source_type, is_contaminated, chlorine_level, tested_by, tested_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (iot_service.sensors[sensor_id]["location"], reading["ph_level"], 
                  reading["turbidity"], reading["bacterial_count"], reading["temperature"],
                  "iot_sensor", reading["is_contaminated"], reading["chlorine_level"], 
                  1, reading["timestamp"]))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error storing IoT reading: {e}")
    
    return reading

@router.get("/iot/sensors")
async def get_all_sensors():
    """Get all registered IoT sensors"""
    return iot_service.get_all_sensors()

@router.get("/iot/contaminated-sources")
async def get_contaminated_sources():
    """Get all contaminated water sources from IoT sensors"""
    return iot_service.get_contaminated_sources()

# Health Education APIs
@router.get("/education/topics")
async def get_education_topics(language: str = "en"):
    """Get all available health education topics"""
    return education_service.get_all_topics(language)

@router.get("/education/content/{topic}")
async def get_education_content(topic: str, language: str = "en"):
    """Get educational content for specific topic"""
    return education_service.get_educational_content(topic, language)

@router.get("/education/campaign/{disease}")
async def get_awareness_campaign(disease: str, language: str = "en"):
    """Get awareness campaign content for specific disease"""
    return education_service.get_awareness_campaign(disease, language)

@router.get("/education/tribal/{topic}")
async def get_tribal_content(topic: str, tribal_language: str):
    """Get educational content in tribal languages"""
    return education_service.get_tribal_language_content(topic, tribal_language)

# Offline Data Management APIs
@router.post("/offline/store")
async def store_offline_data(request: OfflineReportRequest):
    """Store data for offline synchronization"""
    result = offline_service.store_offline_report(request.data, request.report_type)
    return result

@router.post("/offline/sync")
async def sync_offline_data():
    """Synchronize all offline data"""
    result = offline_service.sync_offline_data()
    return result

@router.get("/offline/status")
async def get_offline_status():
    """Get offline queue status"""
    return offline_service.get_offline_queue_status()

# AI/ML Enhanced Prediction APIs
@router.get("/ml/outbreak-prediction/{location}")
async def get_outbreak_prediction(location: str):
    """Get AI-based outbreak prediction for specific location"""
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM health_reports 
            WHERE location LIKE ? AND date(reported_at) >= date('now', '-30 days')
        """, (f"%{location}%",))
        health_reports = cursor.fetchall()
        
        cursor.execute("""
            SELECT * FROM water_quality_reports 
            WHERE location LIKE ? AND date(tested_at) >= date('now', '-30 days')
        """, (f"%{location}%",))
        water_reports = cursor.fetchall()
        
        conn.close()
        
        health_objs = [type('Report', (), dict(zip(['id', 'disease_suspected', 'severity', 'location', 'reported_at'], r))) for r in health_reports]
        water_objs = [type('Report', (), dict(zip(['id', 'location', 'ph_level', 'turbidity', 'bacterial_count', 'temperature', 'source_type', 'is_contaminated', 'tested_at'], r))) for r in water_reports]
        
        prediction = predict_outbreak(health_objs, water_objs, location)
        
        return {
            "location": location,
            "prediction": prediction,
            "data_points": {
                "health_reports": len(health_reports),
                "water_reports": len(water_reports)
            }
        }
    except Exception as e:
        return {"error": str(e)}

# Multi-language Support API
@router.get("/languages/supported")
async def get_supported_languages():
    """Get list of supported languages"""
    return {
        "languages": [
            {"code": "en", "name": "English", "native_name": "English"},
            {"code": "hi", "name": "Hindi", "native_name": "हिन्दी"},
            {"code": "as", "name": "Assamese", "native_name": "অসমীয়া"},
            {"code": "bn", "name": "Bengali", "native_name": "বাংলা"},
            {"code": "ne", "name": "Nepali", "native_name": "नेपाली"},
            {"code": "mni", "name": "Manipuri", "native_name": "মৈতৈলোন্"},
            {"code": "lus", "name": "Mizo", "native_name": "Mizo ṭawng"}
        ]
    }

# Dashboard Enhancement APIs
@router.get("/dashboard/overview")
async def get_dashboard_overview():
    """Get comprehensive dashboard overview"""
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM health_reports WHERE date(reported_at) >= date('now', '-7 days')")
        weekly_reports = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM alerts WHERE is_active = 1")
        active_alerts = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM water_quality_reports WHERE is_contaminated = 1")
        contaminated_sources = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT location) FROM health_reports")
        affected_areas = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "weekly_reports": weekly_reports,
            "active_alerts": active_alerts,
            "contaminated_sources": contaminated_sources,
            "affected_areas": affected_areas,
            "system_status": "operational",
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}