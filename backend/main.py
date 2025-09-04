from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional
import random

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./health_surveillance.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database models
class HealthReport(Base):
    __tablename__ = "health_reports"
    id = Column(Integer, primary_key=True, index=True)
    disease = Column(String)
    severity = Column(String)
    location = Column(String)
    reported_at = Column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    severity = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

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

class HealthReportUpdate(BaseModel):
    disease: Optional[str] = None
    severity: Optional[str] = None
    location: Optional[str] = None

class WaterSourceCreate(BaseModel):
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
    is_active: bool = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_sample_data():
    db = SessionLocal()
    if db.query(HealthReport).count() == 0:
        # UPDATE THESE VALUES:
        diseases = ["diarrhea", "cholera", "typhoid", "hepatitis_a", "dysentery", "gastroenteritis"]
        severities = ["mild", "moderate", "severe"]
        locations = ["Village A", "Village B", "Village C", "Town Center", "Rural Area"]
        
        for _ in range(50):
            report = HealthReport(
                disease=random.choice(diseases),
                severity=random.choice(severities),
                location=random.choice(locations),
                reported_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
            )
            db.add(report)
        
        for _ in range(10):
            alert = Alert(
                severity=random.choice(["low", "medium", "high", "critical"]),
                is_active=random.choice([True, False]),
                created_at=datetime.utcnow() - timedelta(days=random.randint(0, 7))
            )
            db.add(alert)
        
        for _ in range(30):
            source = WaterSource(
                is_safe=random.choice([True, False]),
                ph_level=random.uniform(6.0, 9.0),
                turbidity=random.uniform(0, 10),
                bacterial_count=random.randint(0, 200),
                temperature=random.uniform(15, 35),
                source_type="iot_sensor",
                tested_at=datetime.utcnow() - timedelta(days=random.randint(0, 10))
            )
            db.add(source)
        
        db.commit()
    db.close()

app = FastAPI(title="Health Surveillance API", version="1.0.0")
init_sample_data()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Smart Health Surveillance System API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "health-surveillance-api"}

@app.get("/api/health/reports/stats")
async def get_health_stats(db: Session = Depends(get_db)):
    reports = db.query(HealthReport).all()
    recent_reports = db.query(HealthReport).filter(
        HealthReport.reported_at >= datetime.utcnow() - timedelta(days=7)
    ).all()
    
    by_disease = {}
    by_severity = {"mild": 0, "moderate": 0, "severe": 0}
    
    for report in reports:
        by_disease[report.disease] = by_disease.get(report.disease, 0) + 1
        by_severity[report.severity] += 1
    
    return {
        "total_reports": len(reports),
        "by_disease": by_disease,
        "by_severity": by_severity,
        "recent_reports": len(recent_reports)
    }

@app.get("/api/alerts/stats")
async def get_alert_stats(db: Session = Depends(get_db)):
    active_alerts = db.query(Alert).filter(Alert.is_active == True).all()
    
    by_severity = {"low": 0, "medium": 0, "high": 0, "critical": 0}
    for alert in active_alerts:
        by_severity[alert.severity] += 1
    
    return {
        "total_active_alerts": len(active_alerts),
        "by_severity": by_severity
    }

@app.get("/api/water/reports/stats")
async def get_water_stats(db: Session = Depends(get_db)):
    sources = db.query(WaterSource).all()
    safe_sources = db.query(WaterSource).filter(WaterSource.is_safe == True).all()
    
    return {
        "total_sources": len(sources),
        "safe_sources": len(safe_sources),
        "contaminated_sources": len(sources) - len(safe_sources)
    }

@app.get("/api/water/quality")
async def get_water_quality_reports(db: Session = Depends(get_db)):
    sources = db.query(WaterSource).all()
    return [{
        "id": s.id, 
        "ph_level": s.ph_level, 
        "turbidity": s.turbidity, 
        "bacterial_count": s.bacterial_count, 
        "temperature": s.temperature, 
        "is_safe": s.is_safe, 
        "tested_at": s.tested_at
    } for s in sources]

@app.get("/api/alerts/dashboard")
async def get_alerts_dashboard(db: Session = Depends(get_db)):
    alerts = db.query(Alert).filter(Alert.is_active == True).all()
    return [{
        "id": a.id, 
        "severity": a.severity, 
        "created_at": a.created_at
    } for a in alerts]

# CRUD endpoints for updates
@app.post("/api/health/reports")
async def create_health_report(report: HealthReportCreate, db: Session = Depends(get_db)):
    db_report = HealthReport(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

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
    db_source = WaterSource(**source.dict())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source

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
    db_alert = Alert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

@app.get("/api/sms/send-alert")
async def send_sms_alert(message: str):
    return {"status": "sent", "message": message, "timestamp": datetime.utcnow()}