from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
from datetime import datetime
from services.sms_service import SMSService
from services.iot_service import IoTWaterSensorService
from services.education_service import HealthEducationService
from services.offline_service import OfflineDataService
from services.community_service import CommunityVolunteerService
from services.enhanced_sms_service import EnhancedSMSService
from services.resource_allocation_service import ResourceAllocationService
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ml_models.outbreak_prediction import predict_outbreak

app = FastAPI(title="Smart Health Surveillance & Early Warning System", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
sms_service = SMSService()
iot_service = IoTWaterSensorService()
education_service = HealthEducationService()
offline_service = OfflineDataService()
community_service = CommunityVolunteerService()
enhanced_sms_service = EnhancedSMSService()
resource_service = ResourceAllocationService()

# Pydantic models
class HealthReportCreate(BaseModel):
    disease: str
    severity: str
    location: str
    patient_age: Optional[int] = 25
    patient_gender: Optional[str] = "unknown"

class WaterSourceCreate(BaseModel):
    location: str
    is_safe: bool
    ph_level: float
    turbidity: float
    bacterial_count: int
    temperature: float
    source_type: str

class AlertCreate(BaseModel):
    severity: str
    location: Optional[str] = "Mobile Report"
    message: Optional[str] = "Alert from mobile app"

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

class VolunteerReportRequest(BaseModel):
    reporter_name: str
    location: str
    report_type: str
    description: str
    language: Optional[str] = "en"

class SMSDataRequest(BaseModel):
    phone_numbers: List[str]
    template_type: str
    language: Optional[str] = "en"
    custom_message: Optional[str] = None

class ResourceRequest(BaseModel):
    resource_type: str
    quantity: int
    priority: str
    location: str
    requester_name: Optional[str] = "Mobile User"
    justification: Optional[str] = "Mobile app request"

class EmailAlertRequest(BaseModel):
    email: str
    subject: str
    message: str
    alert_type: str

@app.get("/mobile")
async def mobile_app():
    return FileResponse('mobile.html')

@app.get("/enhanced_mobile")
async def enhanced_mobile_app():
    return FileResponse('enhanced_mobile.html')

@app.get("/enhanced_features")
async def enhanced_features_app():
    return FileResponse('enhanced_mobile_features.html')

@app.get("/enhanced_map")
async def enhanced_map():
    return FileResponse('enhanced_map.html')

@app.get("/")
async def root():
    return {"message": "Smart Health Surveillance System API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "health-surveillance-api"}

@app.post("/api/health/reports")
async def create_health_report(report: HealthReportCreate):
    try:
        # Store health report
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO health_reports 
            (disease, severity, location, reported_at)
            VALUES (?, ?, ?, ?)
        """, (report.disease, report.severity, report.location, datetime.now()))
        conn.commit()
        conn.close()
        
        # Trigger AI prediction for this location
        prediction_result = await trigger_outbreak_prediction(report.location)
        
        response = {"status": "success"}
        if prediction_result.get('alert_generated'):
            response['alert'] = {
                'severity': prediction_result['alert_data'].get('severity'),
                'message': f"Alert: {prediction_result['alert_data'].get('severity')} risk detected in {report.location}"
            }
        
        return response
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/water/sources")
async def create_water_source(source: WaterSourceCreate):
    try:
        # Store water quality report
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO water_quality_reports 
            (location, ph_level, turbidity, bacterial_count, temperature, source_type, 
             is_contaminated, chlorine_level, tested_by, tested_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (source.location, source.ph_level, source.turbidity, source.bacterial_count,
              source.temperature, source.source_type, not source.is_safe, 0.2, 1, datetime.now()))
        conn.commit()
        conn.close()
        
        # Trigger AI prediction for this location
        prediction_result = await trigger_outbreak_prediction(source.location)
        
        response = {"status": "success"}
        if prediction_result.get('alert_generated'):
            response['alert'] = {
                'severity': prediction_result['alert_data'].get('severity'),
                'message': f"Water contamination alert: {prediction_result['alert_data'].get('severity')} risk in {source.location}"
            }
        
        return response
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/alerts")
async def create_alert(alert: AlertCreate):
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alerts 
            (severity, is_active, created_at, location, message)
            VALUES (?, ?, ?, ?, ?)
        """, (alert.severity, 1, datetime.now(), alert.location, alert.message))
        conn.commit()
        conn.close()
        
        # Trigger prediction for alert location
        prediction_result = await trigger_outbreak_prediction(alert.location)
        
        return {"status": "success", "prediction_triggered": prediction_result.get('alert_generated', False)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/health/reports/stats")
async def get_health_stats():
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM health_reports")
        total = cursor.fetchone()[0]
        conn.close()
        return {
            "total_reports": total,
            "by_disease": {"diarrhea": 2, "cholera": 1, "typhoid": 1},
            "by_severity": {"mild": 1, "moderate": 2, "severe": 1},
            "recent_reports": total
        }
    except:
        return {"total_reports": 0, "by_disease": {}, "by_severity": {"mild": 0, "moderate": 0, "severe": 0}, "recent_reports": 0}

@app.get("/api/alerts/stats")
async def get_alert_stats():
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM alerts WHERE is_active = 1")
        total = cursor.fetchone()[0]
        conn.close()
        return {
            "total_active_alerts": total,
            "by_severity": {"low": 0, "medium": 1, "high": 1, "critical": 0}
        }
    except:
        return {"total_active_alerts": 0, "by_severity": {"low": 0, "medium": 0, "high": 0, "critical": 0}}

@app.get("/api/water/reports/stats")
async def get_water_stats():
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM water_quality_reports")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM water_quality_reports WHERE is_contaminated = 0")
        safe = cursor.fetchone()[0]
        conn.close()
        return {
            "total_sources": total,
            "safe_sources": safe,
            "contaminated_sources": total - safe
        }
    except:
        return {"total_sources": 0, "safe_sources": 0, "contaminated_sources": 0}

# Auto-prediction endpoint for testing
@app.post("/api/trigger-prediction/{location}")
async def manual_trigger_prediction(location: str):
    """Manually trigger prediction for testing"""
    result = await trigger_outbreak_prediction(location)
    return result

@app.post("/api/force-email-test/{location}")
async def force_email_test(location: str):
    """Force trigger email for testing with mock high-risk prediction"""
    try:
        from services.email_service import EmailService
        email_service = EmailService()
        
        # Create mock high-risk prediction
        mock_prediction = {
            'location': location,
            'disease': 'cholera',
            'risk_score': 0.85,  # High risk
            'predicted_cases': 15,
            'confidence': 0.78,
            'factors': '["high_water_contamination", "severe_cases_present", "monsoon_season"]'
        }
        
        email_result = email_service.send_risk_alert("niswan0077@gmail.com", mock_prediction)
        return {
            "status": "success",
            "location": location,
            "email_result": email_result,
            "prediction": mock_prediction
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/water/sources")
async def get_water_sources():
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, location, ph_level, turbidity, bacterial_count, temperature, source_type, is_contaminated, tested_at, chlorine_level FROM water_quality_reports ORDER BY id DESC LIMIT 10")
        rows = cursor.fetchall()
        conn.close()
        return [{
            "id": r[0], 
            "location": r[1], 
            "ph_level": r[2], 
            "turbidity": r[3],
            "bacterial_count": r[4],
            "temperature": r[5],
            "source_type": r[6],
            "is_safe": not r[7],
            "tested_at": r[8],
            "chlorine_level": r[9]
        } for r in rows]
    except:
        return []

@app.get("/api/water/quality")
async def get_water_quality_reports():
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, location, ph_level, turbidity, bacterial_count, temperature, source_type, is_contaminated, tested_at, chlorine_level FROM water_quality_reports ORDER BY id DESC LIMIT 10")
        rows = cursor.fetchall()
        conn.close()
        return [{
            "id": r[0], 
            "location": r[1], 
            "ph_level": r[2], 
            "turbidity": r[3],
            "bacterial_count": r[4],
            "temperature": r[5],
            "source_type": r[6],
            "is_safe": not r[7],
            "tested_at": r[8],
            "chlorine_level": r[9]
        } for r in rows]
    except:
        return []

@app.get("/api/alerts")
async def get_alerts():
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, severity, is_active, created_at, location, message 
            FROM alerts 
            ORDER BY id DESC 
            LIMIT 10
        """)
        rows = cursor.fetchall()
        conn.close()
        return [{
            "id": r[0], 
            "severity": r[1],
            "is_active": bool(r[2]),
            "created_at": str(r[3]) if r[3] else "",
            "location": r[4] if len(r) > 4 else "Unknown",
            "message": r[5] if len(r) > 5 else "Health alert"
        } for r in rows]
    except Exception as e:
        print(f"Alerts error: {e}")
        return []

@app.get("/api/health/reports")
async def get_health_reports():
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, disease, severity, location, reported_at FROM health_reports ORDER BY id DESC LIMIT 10")
        rows = cursor.fetchall()
        conn.close()
        return [{
            "id": r[0],
            "disease": r[1],
            "severity": r[2],
            "location": r[3],
            "reported_at": str(r[4]) if r[4] else "",
            "patient_age": 25,  # default values
            "patient_gender": "unknown"
        } for r in rows]
    except Exception as e:
        print(f"Health reports error: {e}")
        return []

@app.get("/api/alerts/dashboard")
async def get_alerts_dashboard():
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, severity, created_at FROM alerts WHERE is_active = 1 ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()
        return [{
            "id": r[0], 
            "severity": r[1], 
            "created_at": str(r[2]) if r[2] else ""
        } for r in rows]
    except Exception as e:
        print(f"Dashboard alerts error: {e}")
        return []

from fastapi import Request
from fastapi.responses import JSONResponse

@app.put("/api/alerts/{alert_id}")
async def update_alert(alert_id: int, request: Request):
    try:
        alert_data = await request.json()
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        
        is_active = 1 if alert_data.get("is_active", True) else 0
        cursor.execute("UPDATE alerts SET is_active = ? WHERE id = ?", (is_active, alert_id))
        
        conn.commit()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.delete("/api/alerts/{alert_id}")
async def delete_alert(alert_id: int):
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alerts WHERE id = ?", (alert_id,))
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Alert deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.delete("/api/health/reports/{report_id}")
async def delete_health_report(report_id: int):
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM health_reports WHERE id = ?", (report_id,))
        # Clear old predictions when data changes
        cursor.execute("DELETE FROM predictions WHERE prediction_date < datetime('now', '-1 hour')")
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Health report deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.delete("/api/water/sources/{source_id}")
async def delete_water_source(source_id: int):
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM water_quality_reports WHERE id = ?", (source_id,))
        # Clear old predictions when data changes
        cursor.execute("DELETE FROM predictions WHERE prediction_date < datetime('now', '-1 hour')")
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Water source deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.put("/api/health/reports/{report_id}/cure")
async def mark_patient_cured(report_id: int):
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM health_reports WHERE id = ?", (report_id,))
        # Clear old predictions when data changes
        cursor.execute("DELETE FROM predictions WHERE prediction_date < datetime('now', '-1 hour')")
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Patient marked as cured"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/sms/send-alert")
async def send_sms_alert(message: str):
    return {"status": "sent", "message": message, "timestamp": datetime.utcnow()}

# AI Predictions API
@app.get("/api/ai/predictions")
async def get_ai_predictions():
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        
        # Auto-cleanup old predictions (older than 2 hours)
        cursor.execute("DELETE FROM predictions WHERE prediction_date < datetime('now', '-2 hours')")
        
        # Get recent predictions from database
        cursor.execute("""
            SELECT location, disease, risk_score, predicted_cases, confidence, factors, prediction_date
            FROM predictions 
            WHERE prediction_date > datetime('now', '-1 hour')
            ORDER BY id DESC 
            LIMIT 10
        """)
        prediction_rows = cursor.fetchall()
        
        conn.commit()
        conn.close()
        
        if len(prediction_rows) == 0:
            return []
        
        # Format for dashboard
        predictions = []
        for i, row in enumerate(prediction_rows):
            location, disease, risk_score, predicted_cases, confidence, factors, prediction_date = row
            
            import json
            try:
                factors_list = json.loads(factors) if factors else []
            except:
                factors_list = []
            
            predictions.append({
                "id": i + 1,
                "disease": disease,
                "location": location,
                "riskScore": int(risk_score * 100),
                "predictedCases": predicted_cases,
                "confidence": int(confidence * 100),
                "factors": factors_list,
                "timeframe": "7-14 days",
                "timestamp": prediction_date
            })
        
        return predictions
    except Exception as e:
        print(f"Prediction error: {e}")
        return []

# Social Media Sentiment API
@app.get("/api/social/sentiment")
async def get_social_sentiment():
    return {
        "health_concern": 0.72,
        "water_quality": 0.58,
        "government_response": 0.34,
        "trending": ["#WaterCrisis", "#HealthAlert", "#CleanWater"],
        "mentions": 1247,
        "sentiment_score": 6.4
    }

# Weather Correlation API
@app.get("/api/weather/correlation")
async def get_weather_correlation():
    return {
        "temperature": 32,
        "humidity": 78,
        "rainfall": 45,
        "risk_factor": "High",
        "forecast": "Monsoon conditions increase waterborne disease risk",
        "correlation_score": 0.85
    }

# Community Engagement API
@app.get("/api/community/engagement")
async def get_community_engagement():
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM health_reports WHERE date(reported_at) = date('now')")
        today_reports = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT location) FROM health_reports")
        active_locations = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "active_reporters": 1247,
            "reports_today": today_reports,
            "verified_reports": int(today_reports * 0.75),
            "community_score": 8.4,
            "active_locations": active_locations
        }
    except:
        return {
            "active_reporters": 1247,
            "reports_today": 0,
            "verified_reports": 0,
            "community_score": 8.4,
            "active_locations": 5
        }

# Hotspots API
@app.get("/api/hotspots")
async def get_hotspots():
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT location, COUNT(*) as cases, severity
            FROM health_reports 
            WHERE date(reported_at) >= date('now', '-7 days')
            GROUP BY location 
            ORDER BY cases DESC
        """)
        
        hotspots = []
        for row in cursor.fetchall():
            location, cases, severity = row
            hotspots.append({
                "location": location,
                "cases": cases,
                "severity": "high" if cases > 5 else "medium" if cases > 2 else "low",
                "lat": 25.0 + len(location) * 0.1,  # Mock coordinates
                "lng": 91.0 + len(location) * 0.1,
                "trend": "increasing" if cases > 3 else "stable"
            })
        
        conn.close()
        return hotspots
    except Exception as e:
        return []

# Interventions API
@app.get("/api/interventions")
async def get_interventions():
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        
        # Get locations with high alert activity
        cursor.execute("""
            SELECT location, COUNT(*) as alert_count
            FROM alerts 
            WHERE is_active = 1
            GROUP BY location
            ORDER BY alert_count DESC
            LIMIT 5
        """)
        
        interventions = []
        for i, (location, count) in enumerate(cursor.fetchall()):
            interventions.append({
                "id": i + 1,
                "location": location or f"Area {i+1}",
                "type": "Emergency Response" if count > 2 else "Preventive Measures",
                "status": "Active" if i < 2 else "Planned",
                "resources": count * 3 + 5,
                "timeline": f"{i + 2} days",
                "priority": "High" if count > 2 else "Medium"
            })
        
        conn.close()
        return interventions
    except:
        return []

# Resource Allocation API
@app.get("/api/resources")
async def get_resource_allocation():
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM alerts WHERE is_active = 1")
        active_alerts = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM health_reports WHERE date(reported_at) >= date('now', '-7 days')")
        recent_reports = cursor.fetchone()[0]
        
        conn.close()
        
        base_need = max(active_alerts * 2, recent_reports)
        
        return [
            {
                "type": "Medical Teams",
                "allocated": min(12, base_need),
                "available": 8,
                "needed": base_need + 3
            },
            {
                "type": "Water Testing Kits",
                "allocated": min(45, base_need * 3),
                "available": 23,
                "needed": base_need * 4
            },
            {
                "type": "Emergency Supplies",
                "allocated": min(200, base_need * 10),
                "available": 150,
                "needed": base_need * 15
            },
            {
                "type": "Vehicles",
                "allocated": min(8, base_need // 2),
                "available": 3,
                "needed": base_need // 2 + 4
            }
        ]
    except:
        return []

# Risk Score API
@app.get("/api/risk-score")
async def get_risk_score():
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM alerts WHERE is_active = 1")
        active_alerts = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM health_reports WHERE date(reported_at) >= date('now', '-3 days')")
        recent_reports = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM water_quality_reports WHERE is_contaminated = 1")
        contaminated_sources = cursor.fetchone()[0]
        
        conn.close()
        
        # Calculate risk score (0-100)
        risk_score = min(100, (active_alerts * 15) + (recent_reports * 5) + (contaminated_sources * 10))
        
        return {
            "score": risk_score,
            "level": "Critical" if risk_score > 80 else "High" if risk_score > 60 else "Medium" if risk_score > 40 else "Low",
            "factors": {
                "active_alerts": active_alerts,
                "recent_reports": recent_reports,
                "contaminated_sources": contaminated_sources
            }
        }
    except:
        return {"score": 45, "level": "Medium", "factors": {}}

# AI Prediction Function
async def trigger_outbreak_prediction(location: str):
    """Automatically trigger AI prediction when new data is added"""
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        
        # Get recent health reports for this EXACT location only
        cursor.execute("""
            SELECT disease, severity, reported_at, location
            FROM health_reports 
            WHERE LOWER(TRIM(location)) = LOWER(TRIM(?)) AND reported_at > datetime('now', '-7 days')
        """, (location,))
        health_reports = [{'disease': r[0], 'severity': r[1], 'reported_at': r[2], 'location': r[3]} 
                         for r in cursor.fetchall()]
        
        # Get recent water quality reports for this EXACT location only
        cursor.execute("""
            SELECT location, ph_level, turbidity, bacterial_count, is_contaminated, tested_at
            FROM water_quality_reports 
            WHERE LOWER(TRIM(location)) = LOWER(TRIM(?)) AND tested_at > datetime('now', '-7 days')
        """, (location,))
        water_reports = [{'location': r[0], 'ph_level': r[1], 'turbidity': r[2],
                         'bacterial_count': r[3], 'is_contaminated': r[4], 'tested_at': r[5]} 
                        for r in cursor.fetchall()]
        
        conn.close()
        
        # Only run prediction if we have data for this specific location
        if len(health_reports) >= 1 or len(water_reports) >= 1:
            print(f"Running prediction for {location}: {len(health_reports)} health reports, {len(water_reports)} water reports")
            from ml_models.outbreak_prediction import predict_outbreak
            prediction = predict_outbreak(health_reports, water_reports, location)
            
            # Store prediction in database
            conn = sqlite3.connect("health_surveillance.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO predictions 
                (location, disease, risk_score, predicted_cases, factors, confidence, prediction_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (location, prediction['disease'], prediction['risk_score'], 
                  prediction['predicted_cases'], str(prediction['factors']), 
                  prediction['confidence'], datetime.now()))
            conn.commit()
            conn.close()
            
            # Create alert if high risk
            if prediction['risk_score'] > 0.5:  # Alert threshold
                risk_pct = int(prediction['risk_score'] * 100)
                if risk_pct >= 80:
                    severity = "critical"
                    alert_msg = f"CRITICAL: {prediction['disease']} outbreak {risk_pct}% risk in {location}"
                elif risk_pct >= 70:
                    severity = "high"
                    alert_msg = f"HIGH: {prediction['disease']} outbreak {risk_pct}% risk in {location}"
                else:
                    severity = "medium"
                    alert_msg = f"MEDIUM: {prediction['disease']} risk {risk_pct}% in {location}"
                
                # Store alert in database
                conn = sqlite3.connect("health_surveillance.db")
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO alerts (severity, is_active, created_at, location, message)
                    VALUES (?, 1, datetime('now'), ?, ?)
                """, (severity, location, alert_msg))
                conn.commit()
                conn.close()
                print(f"Alert created: {severity} for {location}")
            
            # Send email alert if high risk
            if prediction['risk_score'] > 0.6:  # Email threshold
                try:
                    from services.email_service import EmailService
                    email_service = EmailService()
                    
                    # Format prediction data for email
                    import json
                    factors_str = prediction['factors'] if isinstance(prediction['factors'], str) else json.dumps(prediction['factors'])
                    email_prediction_data = {
                        'location': location,
                        'disease': prediction['disease'],
                        'risk_score': prediction['risk_score'],
                        'predicted_cases': prediction['predicted_cases'],
                        'confidence': prediction['confidence'],
                        'factors': factors_str
                    }
                    
                    email_result = email_service.send_risk_alert("niswan0077@gmail.com", email_prediction_data)
                    prediction['email_sent'] = email_result['status'] == 'success'
                    prediction['email_result'] = email_result
                    print(f"Email alert sent: {email_result['status']} for {location} (Risk: {prediction['risk_score']:.1%})")
                    print(f"Email details: {email_result.get('message', 'No message')}")
                except Exception as e:
                    print(f"Email failed: {str(e)}")
                    prediction['email_sent'] = False
                    prediction['email_error'] = str(e)
            
            prediction['alert_generated'] = True
            return prediction
        
        return {'alert_generated': False, 'message': f'No data found for location: {location}'}
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return {'alert_generated': False, 'error': str(e)}

# Emergency Alert System
@app.post("/api/emergency/alert")
async def send_emergency_alert(message: str, phone_numbers: List[str], language: str = "en"):
    """Send emergency health alert"""
    try:
        result = enhanced_sms_service.send_emergency_alert(phone_numbers, message, language)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/email/alert")
async def send_email_alert(request: EmailAlertRequest):
    """Send email alert"""
    try:
        # Store email alert in database
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alerts (severity, is_active, created_at, location, message)
            VALUES (?, ?, ?, ?, ?)
        """, (request.alert_type, 1, datetime.now(), 'Email Alert', f"Email sent to {request.email}: {request.subject}"))
        conn.commit()
        conn.close()
        
        # Simulate email sending (in production, use actual email service)
        return {
            "status": "success",
            "message": f"Email alert sent to {request.email}",
            "subject": request.subject,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Enhanced API Endpoints

# Community Volunteer Reporting
@app.post("/api/community/volunteer-report")
async def submit_volunteer_report(request: VolunteerReportRequest):
    """Submit volunteer report"""
    try:
        result = community_service.submit_volunteer_report({
            'reporter_name': request.reporter_name,
            'location': request.location,
            'report_type': request.report_type,
            'description': request.description,
            'language': request.language
        })
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/community/reports")
async def get_volunteer_reports(status: str = None, limit: int = 50):
    """Get volunteer reports"""
    try:
        reports = community_service.get_volunteer_reports(status=status, limit=limit)
        return reports
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/community/stats")
async def get_community_stats():
    """Get community engagement statistics"""
    try:
        stats = community_service.get_community_stats()
        return stats
    except Exception as e:
        return {"error": str(e)}

# Enhanced SMS Services
@app.post("/api/sms/send-data-request")
async def send_sms_data_request(request: SMSDataRequest):
    """Send SMS data collection request"""
    try:
        if request.custom_message:
            # Use custom message
            result = enhanced_sms_service.send_data_collection_request(
                request.phone_numbers, 'custom', request.language
            )
        else:
            result = enhanced_sms_service.send_data_collection_request(
                request.phone_numbers, request.template_type, request.language
            )
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/sms/process-response")
async def process_sms_response(phone_number: str, message: str):
    """Process incoming SMS response"""
    try:
        result = enhanced_sms_service.process_sms_response(phone_number, message)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/sms/responses")
async def get_sms_responses(limit: int = 50, processed: bool = None):
    """Get SMS responses"""
    try:
        responses = enhanced_sms_service.get_sms_responses(limit=limit, processed=processed)
        return responses
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/sms/statistics")
async def get_sms_statistics():
    """Get SMS service statistics"""
    try:
        stats = enhanced_sms_service.get_sms_statistics()
        return stats
    except Exception as e:
        return {"error": str(e)}

# Resource Allocation
@app.post("/api/resources/request")
async def request_resource(request: ResourceRequest):
    """Submit resource request"""
    try:
        result = resource_service.submit_resource_request({
            'resource_type': request.resource_type,
            'quantity': request.quantity,
            'priority': request.priority,
            'location': request.location,
            'requester_name': request.requester_name,
            'justification': request.justification
        })
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/resources/allocation")
async def get_resource_allocation():
    """Get resource allocation dashboard"""
    try:
        allocation_data = resource_service.get_resource_allocation_dashboard()
        return allocation_data
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/resources/requests")
async def get_resource_requests(status: str = None, priority: str = None, limit: int = 50):
    """Get resource requests"""
    try:
        requests = resource_service.get_resource_requests(status=status, priority=priority, limit=limit)
        return requests
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/resources/approve/{request_id}")
async def approve_resource_request(request_id: int):
    """Approve resource request"""
    try:
        result = resource_service.approve_resource_request(request_id)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/resources/statistics")
async def get_resource_statistics():
    """Get resource allocation statistics"""
    try:
        stats = resource_service.get_resource_statistics()
        return stats
    except Exception as e:
        return {"error": str(e)}

# Enhanced Education Services
@app.get("/api/education/topics")
async def get_education_topics(language: str = "en"):
    """Get educational topics"""
    try:
        topics = education_service.get_all_topics(language)
        return topics
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/education/content/{topic}")
async def get_education_content(topic: str, language: str = "en"):
    """Get educational content for specific topic"""
    try:
        content = education_service.get_educational_content(topic, language)
        return content
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/education/audio/{topic}")
async def get_education_audio(topic: str, language: str = "en"):
    """Get audio content for educational topic (placeholder)"""
    # In real implementation, return audio file or URL
    return {"audio_url": f"/static/audio/{topic}_{language}.mp3", "available": False}

# Offline Data Management
@app.post("/api/offline/store")
async def store_offline_data(request: OfflineReportRequest):
    """Store offline data for later sync"""
    try:
        result = offline_service.store_offline_report(request.data, request.report_type)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/offline/sync")
async def sync_offline_data():
    """Sync all offline data"""
    try:
        result = offline_service.sync_offline_data()
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/offline/status")
async def get_offline_status():
    """Get offline queue status"""
    try:
        status = offline_service.get_offline_queue_status()
        return status
    except Exception as e:
        return {"error": str(e)}

# IoT Water Sensor Integration
@app.get("/api/iot/sensors/{sensor_id}/reading")
async def get_sensor_reading(sensor_id: str):
    """Get water quality reading from IoT sensor"""
    try:
        reading = iot_service.get_sensor_reading(sensor_id)
        return reading
    except Exception as e:
        return {"error": str(e)}

# Test email alert endpoint
@app.get("/api/test-email")
async def test_email_alert(email: str = "niswan0077@gmail.com"):
    """Test email alert functionality"""
    try:
        from services.email_service import EmailService
        email_service = EmailService()
        
        # Test with sample prediction data
        test_prediction = {
            'location': 'Delhi',
            'disease': 'cholera',
            'risk_score': 0.75,
            'predicted_cases': 12,
            'confidence': 0.85,
            'factors': '["high_water_contamination", "monsoon_season"]'
        }
        
        result = email_service.send_risk_alert(email, test_prediction)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/test-email-simple")
async def test_simple_email(email: str = "niswan0077@gmail.com"):
    """Simple email test"""
    try:
        from services.email_service import EmailService
        email_service = EmailService()
        result = email_service.send_test_email(email)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Clear predictions endpoint
@app.delete("/api/predictions/clear")
async def clear_predictions(all: bool = False):
    """Clear old or all predictions"""
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        
        if all:
            cursor.execute("DELETE FROM predictions")
            message = "All predictions cleared"
        else:
            # Clear predictions older than 1 hour
            cursor.execute("DELETE FROM predictions WHERE prediction_date < datetime('now', '-1 hour')")
            message = "Old predictions cleared"
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return {
            "status": "success", 
            "message": message,
            "deleted_count": deleted_count
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Include prediction endpoints with alert system
try:
    from api_predictions import router as prediction_router
    app.include_router(prediction_router, prefix="/api")
except ImportError:
    print("Prediction router not available")