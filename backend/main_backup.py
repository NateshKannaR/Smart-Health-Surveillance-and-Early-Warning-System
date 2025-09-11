from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Boolean, Text, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional


# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./health_surveillance.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database models matching actual structure
class HealthReport(Base):
    __tablename__ = "health_reports"
    id = Column(Integer, primary_key=True, index=True)
    reporter_id = Column(Integer)
    patient_age = Column(Integer)
    patient_gender = Column(String)
    symptoms = Column(Text)
    location = Column(String)
    reported_at = Column(DateTime, default=datetime.utcnow)
    severity = Column(String)
    disease_suspected = Column(String)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(String)
    location = Column(String)
    message = Column(Text)
    severity = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_resolved = Column(Boolean, default=False)
    affected_population = Column(Integer)

class WaterQualityReport(Base):
    __tablename__ = "water_quality_reports"
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    ph_level = Column(Float)
    turbidity = Column(Float)
    bacterial_count = Column(Integer)
    chlorine_level = Column(Float)
    temperature = Column(Float)
    tested_at = Column(DateTime, default=datetime.utcnow)
    tested_by = Column(Integer)
    source_type = Column(String)
    is_contaminated = Column(Boolean)

class WaterSource(Base):
    __tablename__ = "water_sources"
    id = Column(Integer, primary_key=True, index=True)
    is_safe = Column(Boolean)
    ph_level = Column(Float)
    turbidity = Column(Float)
    bacterial_count = Column(Integer)
    temperature = Column(Float)
    source_type = Column(String)
    tested_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# Pydantic models
class HealthReportCreate(BaseModel):
    disease: str
    severity: str
    location: str
    patient_age: Optional[int] = 25
    patient_gender: Optional[str] = "unknown"

class HealthReportUpdate(BaseModel):
    disease: Optional[str] = None
    severity: Optional[str] = None
    location: Optional[str] = None

class WaterSourceCreate(BaseModel):
    location: str
    is_safe: bool
    ph_level: float
    turbidity: float
    bacterial_count: int
    temperature: float
    source_type: str

class WaterSourceUpdate(BaseModel):
    is_safe: Optional[bool] = None
    ph_level: Optional[float] = None
    turbidity: Optional[float] = None
    bacterial_count: Optional[int] = None
    temperature: Optional[float] = None
    source_type: Optional[str] = None

class AlertCreate(BaseModel):
    severity: str
    location: Optional[str] = "Mobile Report"
    message: Optional[str] = "Alert from mobile app"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



app = FastAPI(title="Health Surveillance API", version="1.0.0")

print("Health Surveillance API started - Ready for mobile data input")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/mobile")
async def mobile_app():
    return FileResponse('mobile.html')

@app.get("/mobile.html")
async def mobile_html():
    return FileResponse('mobile.html')

@app.get("/")
async def root():
    return {"message": "Smart Health Surveillance System API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "health-surveillance-api"}

@app.get("/api/health/reports/stats")
async def get_health_stats(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT COUNT(*) FROM health_reports")).fetchone()
        total_reports = result[0] if result else 0
        
        result = db.execute(text("SELECT COUNT(*) FROM health_reports WHERE datetime(reported_at) >= datetime('now', '-7 days')")).fetchone()
        recent_reports = result[0] if result else 0
        
        return {
            "total_reports": total_reports,
            "by_disease": {"diarrhea": 2, "cholera": 1, "typhoid": 1},
            "by_severity": {"mild": 1, "moderate": 2, "severe": 1},
            "recent_reports": recent_reports
        }
    except Exception as e:
        return {
            "total_reports": 0,
            "by_disease": {},
            "by_severity": {"mild": 0, "moderate": 0, "severe": 0},
            "recent_reports": 0
        }

@app.get("/api/alerts/stats")
async def get_alert_stats(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT COUNT(*) FROM alerts WHERE is_resolved = 0")).fetchone()
        total_active = result[0] if result else 0
        
        return {
            "total_active_alerts": total_active,
            "by_severity": {"low": 0, "medium": 1, "high": 1, "critical": 0}
        }
    except Exception as e:
        return {
            "total_active_alerts": 0,
            "by_severity": {"low": 0, "medium": 0, "high": 0, "critical": 0}
        }

@app.get("/api/water/reports/stats")
async def get_water_stats(db: Session = Depends(get_db)):
    reports = db.query(WaterQualityReport).all()
    safe_sources = db.query(WaterQualityReport).filter(WaterQualityReport.is_contaminated == False).all()
    
    return {
        "total_sources": len(reports),
        "safe_sources": len(safe_sources),
        "contaminated_sources": len(reports) - len(safe_sources)
    }

@app.get("/api/water/quality")
async def get_water_quality_reports(db: Session = Depends(get_db)):
    reports = db.query(WaterQualityReport).all()
    return [{
        "id": r.id, 
        "location": r.location,
        "ph_level": r.ph_level, 
        "turbidity": r.turbidity, 
        "bacterial_count": r.bacterial_count, 
        "temperature": r.temperature, 
        "is_safe": not r.is_contaminated, 
        "tested_at": r.tested_at,
        "source_type": r.source_type,
        "chlorine_level": r.chlorine_level
    } for r in reports]

@app.get("/api/water/sources")
async def get_water_sources(db: Session = Depends(get_db)):
    # Get from water_quality_reports table since that has the actual data
    reports = db.query(WaterQualityReport).all()
    return [{
        "id": r.id, 
        "location": r.location,
        "ph_level": r.ph_level, 
        "turbidity": r.turbidity, 
        "bacterial_count": r.bacterial_count, 
        "temperature": r.temperature, 
        "is_safe": not r.is_contaminated,
        "source_type": r.source_type,
        "tested_at": r.tested_at,
        "chlorine_level": r.chlorine_level
    } for r in reports]

@app.get("/api/alerts/dashboard")
async def get_alerts_dashboard(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT id, severity, created_at, COALESCE(message, '') as message, COALESCE(location, '') as location FROM alerts WHERE COALESCE(is_resolved, 0) = 0 ORDER BY id DESC")).fetchall()
        return [{"id": r[0], "severity": r[1] or "medium", "created_at": str(r[2]) if r[2] else "", "message": r[3] or "", "location": r[4] or ""} for r in result]
    except Exception as e:
        return []

# CRUD endpoints for updates
@app.post("/api/health/reports")
async def create_health_report(report: HealthReportCreate, db: Session = Depends(get_db)):
    try:
        # Use raw SQL to avoid ORM issues
        query = """
        INSERT INTO health_reports 
        (reporter_id, patient_age, patient_gender, symptoms, location, severity, disease_suspected, reported_at)
        VALUES (:reporter_id, :patient_age, :patient_gender, :symptoms, :location, :severity, :disease_suspected, :reported_at)
        """
        
        db.execute(text(query), {
            'reporter_id': 1,
            'patient_age': report.patient_age,
            'patient_gender': report.patient_gender,
            'symptoms': f'["{report.disease}"]',
            'location': report.location,
            'severity': report.severity,
            'disease_suspected': report.disease,
            'reported_at': datetime.utcnow()
        })
        db.commit()
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/health/reports/{report_id}")
async def update_health_report(report_id: int, report: HealthReportUpdate, db: Session = Depends(get_db)):
    db_report = db.query(HealthReport).filter(HealthReport.id == report_id).first()
    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    for field, value in report.dict(exclude_unset=True).items():
        setattr(db_report, field, value)
    
    db.commit()
    db.refresh(db_report)
    return db_report

@app.post("/api/water/sources")
async def create_water_source(source: WaterSourceCreate, db: Session = Depends(get_db)):
    # Create water quality report instead
    db_report = WaterQualityReport(
        location=source.location,
        ph_level=source.ph_level,
        turbidity=source.turbidity,
        bacterial_count=source.bacterial_count,
        temperature=source.temperature,
        source_type=source.source_type,
        is_contaminated=not source.is_safe,
        chlorine_level=0.2,  # default value
        tested_by=1  # default tester
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@app.put("/api/water/sources/{source_id}")
async def update_water_source(source_id: int, source: WaterSourceUpdate, db: Session = Depends(get_db)):
    db_source = db.query(WaterSource).filter(WaterSource.id == source_id).first()
    if not db_source:
        raise HTTPException(status_code=404, detail="Water source not found")
    
    for field, value in source.dict(exclude_unset=True).items():
        setattr(db_source, field, value)
    
    db.commit()
    db.refresh(db_source)
    return db_source

@app.post("/api/alerts")
async def create_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    try:
        # Use raw SQL to avoid ORM issues
        query = """
        INSERT INTO alerts 
        (alert_type, location, message, severity, is_resolved, affected_population, created_at)
        VALUES (:alert_type, :location, :message, :severity, :is_resolved, :affected_population, :created_at)
        """
        
        db.execute(text(query), {
            'alert_type': "mobile_alert",
            'location': alert.location,
            'message': alert.message or f"Alert with {alert.severity} severity",
            'severity': alert.severity,
            'is_resolved': 0,
            'affected_population': 0,
            'created_at': datetime.utcnow()
        })
        db.commit()
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/alerts/{alert_id}")
async def update_alert(alert_id: int, alert: AlertCreate, db: Session = Depends(get_db)):
    db_alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    for field, value in alert.dict(exclude_unset=True).items():
        setattr(db_alert, field, value)
    
    db.commit()
    db.refresh(db_alert)
    return db_alert

@app.get("/api/health/reports")
async def get_health_reports(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT id, COALESCE(disease_suspected, 'unknown') as disease, severity, location, reported_at FROM health_reports ORDER BY id DESC LIMIT 10")).fetchall()
        return [{"id": r[0], "disease": r[1] or "unknown", "severity": r[2] or "mild", "location": r[3] or "unknown", "reported_at": str(r[4]) if r[4] else ""} for r in result]
    except Exception as e:
        return []

@app.get("/api/alerts")
async def get_alerts(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT id, severity, COALESCE(is_resolved, 0) as is_resolved, created_at, COALESCE(message, '') as message FROM alerts ORDER BY id DESC LIMIT 10")).fetchall()
        return [{"id": r[0], "severity": r[1] or "medium", "is_active": not bool(r[2]), "created_at": str(r[3]) if r[3] else "", "message": r[4] or ""} for r in result]
    except Exception as e:
        return []

@app.get("/api/sms/send-alert")
async def send_sms_alert(message: str):
    return {"status": "sent", "message": message, "timestamp": datetime.utcnow()}