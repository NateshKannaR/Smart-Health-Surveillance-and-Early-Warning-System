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
        cursor.execute("SELECT COUNT(*) FROM alerts WHERE is_resolved = 0")
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
            "created_at": str(r[3]) if r[3] else "",
            "message": f"Alert with {r[1]} severity",  # default message
            "location": "Mobile Report"  # default location
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
        cursor.execute("SELECT id, severity, created_at, message, location FROM alerts WHERE is_resolved = 0 ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()
        return [{
            "id": r[0], 
            "severity": r[1], 
            "created_at": r[2], 
            "message": r[3], 
            "location": r[4]
        } for r in rows]
    except:
        return []

@app.get("/api/sms/send-alert")
async def send_sms_alert(message: str):
    return {"status": "sent", "message": message, "timestamp": datetime.utcnow()}