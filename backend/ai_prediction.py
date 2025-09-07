# Simple AI/ML Prediction Engine for Water-borne Disease Outbreaks
import json
from datetime import datetime, timedelta
import random

class OutbreakPredictor:
    def __init__(self):
        self.disease_patterns = {
            'diarrhea': {'monsoon_factor': 2.5, 'water_contamination_factor': 3.0},
            'cholera': {'monsoon_factor': 3.0, 'water_contamination_factor': 4.0},
            'typhoid': {'monsoon_factor': 1.8, 'water_contamination_factor': 2.5},
            'hepatitis_a': {'monsoon_factor': 1.5, 'water_contamination_factor': 2.0}
        }
    
    def predict_outbreak(self, health_reports, water_reports, current_season='monsoon'):
        """Simple ML-like prediction based on patterns"""
        
        # Calculate base risk from recent reports
        recent_cases = len([r for r in health_reports if self._is_recent(r['timestamp'])])
        contaminated_sources = len([w for w in water_reports if not w['is_safe']])
        
        # Seasonal adjustment
        seasonal_multiplier = 2.0 if current_season == 'monsoon' else 1.0
        
        # Risk calculation
        base_risk = (recent_cases * 0.3 + contaminated_sources * 0.7) * seasonal_multiplier
        
        # Determine most likely disease
        disease_scores = {}
        for disease, factors in self.disease_patterns.items():
            score = base_risk * factors['water_contamination_factor']
            if current_season == 'monsoon':
                score *= factors['monsoon_factor']
            disease_scores[disease] = score
        
        predicted_disease = max(disease_scores, key=disease_scores.get)
        confidence = min(95, max(50, int(disease_scores[predicted_disease] * 10)))
        
        # Risk level
        if base_risk > 8:
            risk_level = 'CRITICAL'
        elif base_risk > 5:
            risk_level = 'HIGH'
        elif base_risk > 2:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'
        
        return {
            'predicted_disease': predicted_disease,
            'risk_level': risk_level,
            'confidence': confidence,
            'timeline': '7-14 days' if risk_level in ['HIGH', 'CRITICAL'] else '2-4 weeks',
            'recommendations': self._get_recommendations(predicted_disease, risk_level)
        }
    
    def identify_hotspots(self, health_reports):
        """Identify geographic hotspots"""
        location_counts = {}
        for report in health_reports:
            if self._is_recent(report['timestamp']):
                location = report['location']
                location_counts[location] = location_counts.get(location, 0) + 1
        
        # Sort by case count
        hotspots = sorted(location_counts.items(), key=lambda x: x[1], reverse=True)
        
        return [{
            'location': loc,
            'case_count': count,
            'risk_level': 'HIGH' if count > 10 else 'MEDIUM' if count > 5 else 'LOW'
        } for loc, count in hotspots[:5]]
    
    def _is_recent(self, timestamp_str):
        """Check if timestamp is within last 30 days"""
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return (datetime.now() - timestamp).days <= 30
        except:
            return False
    
    def _get_recommendations(self, disease, risk_level):
        """Get intervention recommendations"""
        base_recommendations = [
            "Increase water quality monitoring",
            "Distribute ORS packets to affected areas",
            "Launch hygiene awareness campaigns"
        ]
        
        if risk_level in ['HIGH', 'CRITICAL']:
            base_recommendations.extend([
                "Deploy additional medical teams",
                "Set up temporary treatment centers",
                "Issue public health alerts"
            ])
        
        if disease == 'cholera':
            base_recommendations.append("Implement strict water source isolation")
        elif disease == 'typhoid':
            base_recommendations.append("Focus on food safety inspections")
        
        return base_recommendations

# Usage example
if __name__ == "__main__":
    predictor = OutbreakPredictor()
    
    # Sample data
    health_reports = [
        {'disease': 'diarrhea', 'location': 'Guwahati', 'timestamp': '2024-01-15T10:00:00Z'},
        {'disease': 'cholera', 'location': 'Dibrugarh', 'timestamp': '2024-01-14T15:30:00Z'}
    ]
    
    water_reports = [
        {'location': 'Guwahati', 'is_safe': False, 'ph_level': 8.5},
        {'location': 'Silchar', 'is_safe': True, 'ph_level': 7.2}
    ]
    
    prediction = predictor.predict_outbreak(health_reports, water_reports)
    hotspots = predictor.identify_hotspots(health_reports)
    
    print("Outbreak Prediction:", json.dumps(prediction, indent=2))
    print("Hotspots:", json.dumps(hotspots, indent=2))