import json
from typing import List

# Disease symptom mapping for basic classification
DISEASE_SYMPTOMS = {
    "diarrhea": ["loose_stool", "frequent_bowel", "abdominal_pain", "dehydration"],
    "cholera": ["severe_diarrhea", "vomiting", "dehydration", "muscle_cramps"],
    "typhoid": ["fever", "headache", "abdominal_pain", "rose_spots", "weakness"],
    "hepatitis_a": ["jaundice", "fatigue", "nausea", "abdominal_pain", "dark_urine"],
    "dysentery": ["bloody_stool", "fever", "abdominal_cramps", "tenesmus"],
    "gastroenteritis": ["nausea", "vomiting", "diarrhea", "stomach_cramps"]
}

def analyze_symptoms(symptoms: List[str]) -> str:
    """Analyze symptoms and predict most likely disease"""
    symptom_scores = {}
    
    for disease, disease_symptoms in DISEASE_SYMPTOMS.items():
        score = 0
        for symptom in symptoms:
            if symptom.lower() in [s.lower() for s in disease_symptoms]:
                score += 1
        
        if score > 0:
            symptom_scores[disease] = score / len(disease_symptoms)
    
    if not symptom_scores:
        return "unknown"
    
    # Return disease with highest score
    return max(symptom_scores, key=symptom_scores.get)

def calculate_severity_score(symptoms: List[str], age: int) -> float:
    """Calculate severity score based on symptoms and patient age"""
    base_score = len(symptoms) * 0.1
    
    # Age factor (higher risk for children and elderly)
    if age < 5 or age > 65:
        age_factor = 1.5
    elif age < 15 or age > 50:
        age_factor = 1.2
    else:
        age_factor = 1.0
    
    # Severe symptoms
    severe_symptoms = ["severe_diarrhea", "high_fever", "severe_dehydration", "bloody_stool"]
    severe_count = sum(1 for s in symptoms if s in severe_symptoms)
    
    severity_score = (base_score + severe_count * 0.3) * age_factor
    return min(severity_score, 1.0)  # Cap at 1.0