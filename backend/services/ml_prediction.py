import json
from datetime import datetime
from typing import List, Dict

def predict_outbreak(health_reports: List, water_reports: List, location: str) -> Dict:
    """Simple outbreak prediction without ML dependencies"""
    
    # Basic analysis without ML
    total_reports = len(health_reports)
    
    if total_reports == 0:
        return {
            "disease": "none",
            "risk_score": 0.0,
            "predicted_cases": 0,
            "factors": json.dumps([]),
            "confidence": 0.0
        }
    
    # Count diseases
    disease_counts = {}
    for report in health_reports:
        disease = getattr(report, 'disease_suspected', 'unknown') or 'unknown'
        disease_counts[disease] = disease_counts.get(disease, 0) + 1
    
    primary_disease = max(disease_counts, key=disease_counts.get) if disease_counts else 'diarrhea'
    
    # Calculate risk factors
    risk_factors = []
    base_risk = min(total_reports * 0.1, 0.8)  # Cap at 0.8
    
    # Water contamination factor
    if water_reports:
        contaminated = sum(1 for w in water_reports if getattr(w, 'is_contaminated', False))
        contamination_rate = contaminated / len(water_reports)
        
        if contamination_rate > 0.5:
            base_risk += 0.3
            risk_factors.append("high_water_contamination")
        elif contamination_rate > 0.2:
            base_risk += 0.15
            risk_factors.append("moderate_water_contamination")
    
    # Report frequency factor
    if total_reports > 10:
        base_risk += 0.2
        risk_factors.append("high_report_frequency")
    elif total_reports > 5:
        base_risk += 0.1
        risk_factors.append("moderate_report_frequency")
    
    # Seasonal factor
    current_month = datetime.now().month
    if current_month in [6, 7, 8, 9]:  # Monsoon months
        base_risk += 0.15
        risk_factors.append("monsoon_season")
    
    # Predicted cases
    predicted_cases = int(total_reports * 1.5)
    
    return {
        "disease": primary_disease,
        "risk_score": min(base_risk, 1.0),
        "predicted_cases": predicted_cases,
        "factors": json.dumps(risk_factors),
        "confidence": min(0.9, 0.3 + (total_reports * 0.05))
    }