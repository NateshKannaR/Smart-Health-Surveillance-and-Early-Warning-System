def analyze_water_quality(ph: float, turbidity: float, bacterial_count: int, chlorine: float) -> bool:
    """Analyze water quality parameters and determine if water is contaminated"""
    
    # WHO standards for drinking water
    contamination_factors = []
    
    # pH should be between 6.5 and 8.5
    if ph < 6.5 or ph > 8.5:
        contamination_factors.append("ph_out_of_range")
    
    # Turbidity should be less than 5 NTU
    if turbidity > 5:
        contamination_factors.append("high_turbidity")
    
    # Bacterial count should be 0 for drinking water
    if bacterial_count > 0:
        contamination_factors.append("bacterial_contamination")
    
    # Free chlorine should be between 0.2-0.5 mg/L for treated water
    if chlorine < 0.2:
        contamination_factors.append("insufficient_chlorine")
    elif chlorine > 2.0:
        contamination_factors.append("excessive_chlorine")
    
    # Water is contaminated if any factor is present
    return len(contamination_factors) > 0

def calculate_contamination_risk(ph: float, turbidity: float, bacterial_count: int, chlorine: float) -> dict:
    """Calculate detailed contamination risk assessment"""
    
    risk_score = 0
    risk_factors = []
    
    # pH risk
    if ph < 6.0 or ph > 9.0:
        risk_score += 0.3
        risk_factors.append("extreme_ph")
    elif ph < 6.5 or ph > 8.5:
        risk_score += 0.1
        risk_factors.append("suboptimal_ph")
    
    # Turbidity risk
    if turbidity > 10:
        risk_score += 0.4
        risk_factors.append("very_high_turbidity")
    elif turbidity > 5:
        risk_score += 0.2
        risk_factors.append("high_turbidity")
    
    # Bacterial contamination risk
    if bacterial_count > 100:
        risk_score += 0.5
        risk_factors.append("severe_bacterial_contamination")
    elif bacterial_count > 10:
        risk_score += 0.3
        risk_factors.append("moderate_bacterial_contamination")
    elif bacterial_count > 0:
        risk_score += 0.1
        risk_factors.append("bacterial_presence")
    
    # Chlorine risk
    if chlorine < 0.1:
        risk_score += 0.2
        risk_factors.append("no_disinfection")
    elif chlorine > 5.0:
        risk_score += 0.1
        risk_factors.append("over_chlorination")
    
    risk_level = "low"
    if risk_score >= 0.7:
        risk_level = "critical"
    elif risk_score >= 0.4:
        risk_level = "high"
    elif risk_score >= 0.2:
        risk_level = "medium"
    
    return {
        "risk_score": min(risk_score, 1.0),
        "risk_level": risk_level,
        "risk_factors": risk_factors,
        "is_safe": risk_score < 0.2
    }