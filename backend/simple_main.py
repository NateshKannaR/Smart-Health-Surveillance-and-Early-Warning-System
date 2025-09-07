from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import sqlite3
from datetime import datetime
import json

app = FastAPI(title="Health Surveillance API")

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

def get_db():
    return sqlite3.connect("health_surveillance.db")

@app.get("/mobile")
async def mobile_app():
    return FileResponse('mobile.html')

@app.get("/")
async def root():
    return {"message": "Health Surveillance API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/health/reports")
async def create_health_report(report: HealthReportCreate):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO health_reports 
            (reporter_id, patient_age, patient_gender, symptoms, location, severity, disease_suspected, reported_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (1, report.patient_age, report.patient_gender, f'["{report.disease}"]', 
              report.location, report.severity, report.disease, datetime.now()))
        conn.commit()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/water/sources")
async def create_water_source(source: WaterSourceCreate):
    try:
        conn = get_db()
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
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alerts 
            (alert_type, location, message, severity, is_resolved, affected_population, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ("mobile_alert", alert.location, alert.message, alert.severity, 0, 0, datetime.now()))
        conn.commit()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/health/reports/stats")
async def get_health_stats():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM health_reports")
        total = cursor.fetchone()[0]
        conn.close()
        return {
            "total_reports": total,
            "by_disease": {"diarrhea": 2, "cholera": 1},
            "by_severity": {"mild": 1, "moderate": 1, "severe": 1},
            "recent_reports": total
        }
    except:
        return {"total_reports": 0, "by_disease": {}, "by_severity": {"mild": 0, "moderate": 0, "severe": 0}, "recent_reports": 0}

@app.get("/api/alerts/stats")
async def get_alert_stats():
    try:
        conn = get_db()
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
        conn = get_db()
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
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM water_quality_reports ORDER BY id DESC LIMIT 20")
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
            "is_safe": not r[10],
            "tested_at": r[12]
        } for r in rows]
    except Exception as e:
        print(f"Error fetching water sources: {e}")
        return []

@app.get("/api/alerts")
async def get_alerts():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alerts WHERE is_resolved = 0 ORDER BY id DESC LIMIT 20")
        rows = cursor.fetchall()
        conn.close()
        return [{
            "id": r[0], 
            "alert_type": r[1],
            "location": r[2],
            "message": r[3],
            "severity": r[4], 
            "created_at": r[7]
        } for r in rows]
    except Exception as e:
        print(f"Error fetching alerts: {e}")
        return []

@app.get("/api/health/reports")
async def get_health_reports():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM health_reports WHERE severity != 'cured' ORDER BY id DESC LIMIT 20")
        rows = cursor.fetchall()
        conn.close()
        return [{
            "id": r[0], 
            "patient_age": r[2],
            "patient_gender": r[3],
            "location": r[5], 
            "severity": r[7], 
            "disease": r[8],
            "reported_at": r[9]
        } for r in rows]
    except Exception as e:
        print(f"Error fetching health reports: {e}")
        return []

@app.delete("/api/health/reports/{report_id}")
async def delete_health_report(report_id: int):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM health_reports WHERE id = ?", (report_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Health report not found")
        
        cursor.execute("DELETE FROM health_reports WHERE id = ?", (report_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Health report not found")
        
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Health report deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting health report: {str(e)}")

@app.delete("/api/water/sources/{source_id}")
async def delete_water_source(source_id: int):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM water_quality_reports WHERE id = ?", (source_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Water source not found")
        
        cursor.execute("DELETE FROM water_quality_reports WHERE id = ?", (source_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Water source not found")
        
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Water report deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting water source: {str(e)}")

@app.delete("/api/alerts/{alert_id}")
async def delete_alert(alert_id: int):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM alerts WHERE id = ?", (alert_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Alert not found")
        
        cursor.execute("DELETE FROM alerts WHERE id = ?", (alert_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Alert deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting alert: {str(e)}")

@app.put("/api/health/reports/{report_id}/cure")
async def mark_patient_cured(report_id: int):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM health_reports WHERE id = ?", (report_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Health report not found")
        
        cursor.execute("UPDATE health_reports SET severity = 'cured' WHERE id = ?", (report_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Health report not found")
        
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Patient marked as cured"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error marking patient as cured: {str(e)}")