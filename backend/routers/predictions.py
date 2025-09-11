from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from backend.models.models import Prediction, HealthReport, WaterQualityReport
from backend.services.ml_prediction import predict_outbreak
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/outbreak")
async def predict_disease_outbreak(location: str, db: Session = Depends(get_db)):
    # Get recent health reports and water quality data
    recent_reports = db.query(HealthReport).filter(
        HealthReport.location.contains(location),
        HealthReport.reported_at >= datetime.utcnow() - timedelta(days=30)
    ).all()
    
    water_reports = db.query(WaterQualityReport).filter(
        WaterQualityReport.location.contains(location),
        WaterQualityReport.tested_at >= datetime.utcnow() - timedelta(days=30)
    ).all()
    
    # Run ML prediction
    prediction_result = predict_outbreak(recent_reports, water_reports, location)
    
    # Store prediction
    db_prediction = Prediction(
        location=location,
        disease=prediction_result["disease"],
        risk_score=prediction_result["risk_score"],
        predicted_cases=prediction_result["predicted_cases"],
        factors=prediction_result["factors"],
        confidence=prediction_result["confidence"]
    )
    
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    
    return db_prediction

@router.get("/risk-assessment")
async def get_risk_assessment(location: str = None, db: Session = Depends(get_db)):
    query = db.query(Prediction)
    if location:
        query = query.filter(Prediction.location.contains(location))
    
    predictions = query.filter(
        Prediction.prediction_date >= datetime.utcnow() - timedelta(days=7)
    ).all()
    
    risk_assessment = {
        "high_risk_areas": [],
        "medium_risk_areas": [],
        "low_risk_areas": [],
        "overall_risk": "low"
    }
    
    for pred in predictions:
        area_info = {
            "location": pred.location,
            "disease": pred.disease,
            "risk_score": pred.risk_score,
            "predicted_cases": pred.predicted_cases
        }
        
        if pred.risk_score >= 0.7:
            risk_assessment["high_risk_areas"].append(area_info)
        elif pred.risk_score >= 0.4:
            risk_assessment["medium_risk_areas"].append(area_info)
        else:
            risk_assessment["low_risk_areas"].append(area_info)
    
    # Determine overall risk
    if risk_assessment["high_risk_areas"]:
        risk_assessment["overall_risk"] = "high"
    elif risk_assessment["medium_risk_areas"]:
        risk_assessment["overall_risk"] = "medium"
    
    return risk_assessment