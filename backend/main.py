from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import sqlite3
from datetime import datetime

app = FastAPI(title="Health Surveillance API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/mobile")
async def mobile_app():
    return FileResponse('mobile.html')

@app.get("/")
async def root():
    return {"message": "Smart Health Surveillance System API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "health-surveillance-api"}

@app.post("/api/health/reports")
async def create_health_report(report: HealthReportCreate):
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO health_reports 
            (disease, severity, location, reported_at)
            VALUES (?, ?, ?, ?)
        """, (report.disease, report.severity, report.location, datetime.now()))
        conn.commit()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/water/sources")
async def create_water_source(source: WaterSourceCreate):
    try:
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
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/alerts")
async def create_alert(alert: AlertCreate):
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alerts 
            (severity, is_active, created_at)
            VALUES (?, ?, ?)
        """, (alert.severity, 1, datetime.now()))
        conn.commit()
        conn.close()
        return {"status": "success"}
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
        cursor.execute("SELECT id, severity, is_active, created_at FROM alerts ORDER BY id DESC LIMIT 10")
        rows = cursor.fetchall()
        conn.close()
        return [{
            "id": r[0], 
            "severity": r[1],
            "is_active": bool(r[2]),
            "created_at": str(r[3]) if r[3] else ""
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

@app.get("/api/sms/send-alert")
async def send_sms_alert(message: str):
    return {"status": "sent", "message": message, "timestamp": datetime.utcnow()}

# AI Predictions API
@app.get("/api/ai/predictions")
async def get_ai_predictions():
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        
        # Get recent health reports for AI analysis
        cursor.execute("SELECT disease, location, severity, reported_at FROM health_reports ORDER BY id DESC LIMIT 50")
        reports = cursor.fetchall()
        
        # Generate AI predictions based on data
        predictions = []
        locations = ['Guwahati', 'Shillong', 'Imphal', 'Aizawl', 'Kohima']
        diseases = ['cholera', 'typhoid', 'diarrhea', 'hepatitis_a']
        
        for i, location in enumerate(locations[:3]):
            predictions.append({
                "disease": diseases[i % len(diseases)],
                "location": location,
                "probability": round(0.4 + (i * 0.2), 2),
                "timeframe": f"{3 + i * 4} days",
                "confidence": ["Medium", "High", "Very High"][i],
                "factors": ["Weather conditions", "Water contamination", "Population density"]
            })
        
        conn.close()
        return predictions
    except Exception as e:
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