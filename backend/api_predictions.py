from fastapi import APIRouter
import sqlite3
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ml_models.outbreak_prediction import predict_outbreak

router = APIRouter()

@router.get("/predictions/{location}")
async def get_outbreak_prediction(location: str):
    """Get AI-powered outbreak prediction with alert system"""
    try:
        conn = sqlite3.connect("health_surveillance.db")
        cursor = conn.cursor()
        
        # Get recent health reports
        cursor.execute("""
            SELECT disease, severity, reported_at, location
            FROM health_reports 
            WHERE location LIKE ? AND reported_at > datetime('now', '-30 days')
        """, (f"%{location}%",))
        health_reports = [{'disease': r[0], 'severity': r[1], 'reported_at': r[2], 'location': r[3]} 
                         for r in cursor.fetchall()]
        
        # Get recent water quality reports
        cursor.execute("""
            SELECT location, ph_level, turbidity, bacterial_count, is_contaminated, tested_at
            FROM water_quality_reports 
            WHERE location LIKE ? AND tested_at > datetime('now', '-30 days')
        """, (f"%{location}%",))
        water_reports = [{'location': r[0], 'ph_level': r[1], 'turbidity': r[2],
                         'bacterial_count': r[3], 'is_contaminated': r[4], 'tested_at': r[5]} 
                        for r in cursor.fetchall()]
        
        conn.close()
        
        # Get AI prediction with integrated alert system
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
        
        return prediction
        
    except Exception as e:
        return {"error": str(e), "risk_score": 0.1, "predicted_cases": 0}