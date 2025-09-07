import json
from datetime import datetime
from typing import List, Dict

def predict_outbreak(health_reports: List, water_reports: List, location: str) -> Dict:
    """AI-based outbreak prediction using health and water data"""
    
    # Basic analysis
    total_reports = len(health_reports)
    
    if total_reports == 0:
        return {
            "disease": "none",
            "risk_score": 0.0,
            "predicted_cases": 0,
            "factors": json.dumps([]),
            "confidence": 0.0
        }
    
    # Analyze disease patterns
    disease_counts = {}
    severity_counts = {'mild': 0, 'moderate': 0, 'severe': 0}
    
    for report in health_reports:
        # Handle both database rows and objects
        if hasattr(report, 'disease'):
            disease = report.disease or 'unknown'
            severity = getattr(report, 'severity', 'mild')
        else:
            disease = report[1] if len(report) > 1 else 'unknown'  # disease column
            severity = report[2] if len(report) > 2 else 'mild'     # severity column
            
        disease_counts[disease] = disease_counts.get(disease, 0) + 1
        if severity in severity_counts:
            severity_counts[severity] += 1
    
    primary_disease = max(disease_counts, key=disease_counts.get) if disease_counts else 'diarrhea'
    severe_cases = severity_counts['severe'] + severity_counts['moderate']
    
    # Calculate risk factors
    risk_factors = []
    base_risk = min(total_reports * 0.1, 0.8)  # Cap at 0.8
    
    # Enhanced water quality analysis
    contaminated_sources = 0
    avg_ph = 7.0
    avg_bacterial_count = 0
    
    if water_reports:
        ph_values = []
        bacterial_counts = []
        
        for w in water_reports:
            # Handle both database rows and objects
            if hasattr(w, 'is_contaminated'):
                if w.is_contaminated:
                    contaminated_sources += 1
                ph_values.append(getattr(w, 'ph_level', 7.0))
                bacterial_counts.append(getattr(w, 'bacterial_count', 0))
            else:
                # Database row format: [id, location, ph_level, turbidity, bacterial_count, ...]
                if len(w) > 7 and w[7]:  # is_contaminated column
                    contaminated_sources += 1
                if len(w) > 2:
                    ph_values.append(w[2] or 7.0)  # ph_level
                if len(w) > 4:
                    bacterial_counts.append(w[4] or 0)  # bacterial_count
        
        if ph_values:
            avg_ph = sum(ph_values) / len(ph_values)
        if bacterial_counts:
            avg_bacterial_count = sum(bacterial_counts) / len(bacterial_counts)
            
        contamination_rate = contaminated_sources / len(water_reports)
        
        # Risk assessment based on water quality
        if contamination_rate > 0.5 or avg_bacterial_count > 500:
            base_risk += 0.4
            risk_factors.append("high_water_contamination")
        elif contamination_rate > 0.2 or avg_bacterial_count > 100:
            base_risk += 0.2
            risk_factors.append("moderate_water_contamination")
            
        # pH factor
        if avg_ph < 6.5 or avg_ph > 8.5:
            base_risk += 0.1
            risk_factors.append("unsafe_ph_levels")
    
    # Enhanced risk factors
    if total_reports > 10:
        base_risk += 0.25
        risk_factors.append("high_report_frequency")
    elif total_reports > 5:
        base_risk += 0.15
        risk_factors.append("moderate_report_frequency")
        
    # Severity factor
    if severe_cases > total_reports * 0.3:
        base_risk += 0.2
        risk_factors.append("high_severity_cases")
        
    # Disease-specific risk
    high_risk_diseases = ['cholera', 'typhoid', 'dysentery']
    if primary_disease in high_risk_diseases:
        base_risk += 0.15
        risk_factors.append(f"high_risk_disease_{primary_disease}")
        
    # Location clustering (same location multiple reports)
    location_reports = {}
    for report in health_reports:
        loc = getattr(report, 'location', '') if hasattr(report, 'location') else (report[3] if len(report) > 3 else '')
        if loc:
            location_reports[loc] = location_reports.get(loc, 0) + 1
    
    max_location_reports = max(location_reports.values()) if location_reports else 0
    if max_location_reports > 3:
        base_risk += 0.2
        risk_factors.append("location_clustering")
    
    # Seasonal factor
    current_month = datetime.now().month
    if current_month in [6, 7, 8, 9]:  # Monsoon months
        base_risk += 0.15
        risk_factors.append("monsoon_season")
    
    # Advanced prediction calculations
    growth_factor = 1.5
    if base_risk > 0.7:
        growth_factor = 2.5
    elif base_risk > 0.5:
        growth_factor = 2.0
        
    predicted_cases = max(int(total_reports * growth_factor), total_reports + 1)
    
    # Confidence based on data quality and quantity
    confidence = 0.3  # base confidence
    confidence += min(0.4, total_reports * 0.05)  # data quantity
    confidence += 0.2 if len(water_reports) > 0 else 0  # water data available
    confidence += 0.1 if len(risk_factors) > 2 else 0  # multiple risk factors
    
    return {
        "disease": primary_disease,
        "risk_score": min(base_risk, 1.0),
        "predicted_cases": predicted_cases,
        "factors": json.dumps(risk_factors),
        "confidence": min(0.95, confidence),
        "data_points": {
            "health_reports": total_reports,
            "water_reports": len(water_reports),
            "contaminated_sources": contaminated_sources,
            "avg_ph": round(avg_ph, 2),
            "avg_bacterial_count": int(avg_bacterial_count)
        }
    }