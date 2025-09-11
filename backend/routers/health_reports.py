from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from database.database import get_db
from models.models import HealthReport, User
from schemas.health_schemas import HealthReportCreate, HealthReportResponse
# from services.ml_service import analyze_symptoms

def analyze_symptoms(symptoms):
    """Simple symptom analysis"""
    symptom_map = {
        'fever': ['typhoid', 'malaria'],
        'diarrhea': ['diarrhea', 'cholera'],
        'vomiting': ['gastroenteritis', 'cholera'],
        'bloody_stool': ['dysentery'],
        'jaundice': ['hepatitis_a']
    }
    
    for symptom in symptoms:
        if symptom in symptom_map:
            return symptom_map[symptom][0]
    return 'unknown'
import json
from datetime import datetime

router = APIRouter()

@router.post("/reports", response_model=HealthReportResponse)
async def create_health_report(report: HealthReportCreate, db: Session = Depends(get_db)):
    # Analyze symptoms using ML
    disease_prediction = analyze_symptoms(report.symptoms)
    
    db_report = HealthReport(
        reporter_id=report.reporter_id,
        patient_age=report.patient_age,
        patient_gender=report.patient_gender,
        symptoms=json.dumps(report.symptoms),
        location=report.location,
        severity=report.severity,
        disease_suspected=disease_prediction
    )
    
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    
    return db_report

@router.get("/reports")
async def get_health_reports(location: str = None, db: Session = Depends(get_db)):
    query = db.query(HealthReport)
    if location:
        query = query.filter(HealthReport.location.contains(location))
    return query.all()

@router.get("/reports/stats")
async def get_health_stats(location: str = None, db: Session = Depends(get_db)):
    query = db.query(HealthReport)
    if location:
        query = query.filter(HealthReport.location.contains(location))
    
    reports = query.all()
    
    stats = {
        "total_reports": len(reports),
        "by_disease": {},
        "by_severity": {"mild": 0, "moderate": 0, "severe": 0},
        "recent_reports": len([r for r in reports if (datetime.now() - r.reported_at).days <= 7])
    }
    
    for report in reports:
        if report.disease_suspected:
            stats["by_disease"][report.disease_suspected] = stats["by_disease"].get(report.disease_suspected, 0) + 1
        stats["by_severity"][report.severity] += 1
    
    return stats