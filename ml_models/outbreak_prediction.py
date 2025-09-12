from datetime import datetime

class OutbreakPredictor:
    def __init__(self):
        self.is_trained = True  # Always ready for rule-based predictions

    def _health_features(self, health_reports):
        disease_counts = {}
        severity_counts = {'mild': 0, 'moderate': 0, 'severe': 0}
        age_groups = {'0-5': 0, '6-18': 0, '19-65': 0, '65+': 0}

        for report in health_reports:
            disease = report.get('disease', 'unknown')
            disease_counts[disease] = disease_counts.get(disease, 0) + 1

            severity = report.get('severity', 'mild')
            if severity in severity_counts:
                severity_counts[severity] += 1

            age = report.get('patient_age', 25)
            if age <= 5:
                age_groups['0-5'] += 1
            elif age <= 18:
                age_groups['6-18'] += 1
            elif age <= 65:
                age_groups['19-65'] += 1
            else:
                age_groups['65+'] += 1

        return {
            'total_reports': len(health_reports),
            'diarrhea_cases': disease_counts.get('diarrhea', 0),
            'cholera_cases': disease_counts.get('cholera', 0),
            'typhoid_cases': disease_counts.get('typhoid', 0),
            'severe_cases': severity_counts['severe'],
            'moderate_cases': severity_counts['moderate'],
            'vulnerable_age_cases': age_groups['0-5'] + age_groups['65+']
        }

    def _water_features(self, water_reports):
        if not water_reports:
            return {
                'contaminated_sources': 0, 'contamination_rate': 0,
                'avg_ph_deviation': 0, 'avg_turbidity': 0, 'avg_bacterial_count': 0
            }

        contaminated_count = sum(1 for w in water_reports if w.get('is_contaminated', False))
        ph_levels = [w.get('ph_level', 7.0) for w in water_reports]
        avg_ph = sum(ph_levels) / len(ph_levels) if ph_levels else 7.0
        
        turbidity_values = [w.get('turbidity', 0) for w in water_reports]
        avg_turbidity = sum(turbidity_values) / len(turbidity_values) if turbidity_values else 0
        
        bacterial_counts = [w.get('bacterial_count', 0) for w in water_reports]
        avg_bacterial = sum(bacterial_counts) / len(bacterial_counts) if bacterial_counts else 0

        return {
            'contaminated_sources': contaminated_count,
            'contamination_rate': contaminated_count / len(water_reports) if water_reports else 0,
            'avg_ph_deviation': abs(avg_ph - 7.0),
            'avg_turbidity': avg_turbidity,
            'avg_bacterial_count': avg_bacterial
        }

    def prepare_features(self, health_reports, water_reports, location_data):
        features = {}
        features.update(self._health_features(health_reports))
        features.update(self._water_features(water_reports))

        current_month = datetime.now().month
        features.update({
            'is_monsoon': 1 if current_month in [6, 7, 8, 9] else 0,
            'is_winter': 1 if current_month in [12, 1, 2] else 0,
            'month': current_month,
            'population_density': location_data.get('population_density', 500)
        })

        return features

    def train_model(self, training_data=None):
        # Rule-based system doesn't need training
        self.is_trained = True
        return {"status": "trained"}

    def predict_outbreak(self, health_reports, water_reports, location):
        # Use rule-based prediction based on actual data only
        if isinstance(location, str):
            location_data = {'population_density': 500}
        else:
            location_data = location

        features = self.prepare_features(health_reports, water_reports, location_data)
        
        # Simple rule-based risk calculation
        risk_score = 0.0
        risk_factors = []
        
        # Only calculate risk if there are actual reports
        if features['total_reports'] == 0:
            risk_score = 0.05  # Very low baseline risk
        else:
            # Base risk from number of reports
            risk_score = min(0.3, features['total_reports'] * 0.05)
            
            # Severity multiplier
            if features['severe_cases'] > 0:
                risk_score += 0.2
                risk_factors.append('severe_cases_present')
            
            # Disease-specific risk
            if features['cholera_cases'] > 0:
                risk_score += 0.25
            elif features['typhoid_cases'] > 0:
                risk_score += 0.15
            
            # Water contamination
            if features['contamination_rate'] > 0.5:
                risk_score += 0.2
                risk_factors.append('high_water_contamination')
            
            # Seasonal factor
            if features['is_monsoon']:
                risk_score += 0.1
                risk_factors.append('monsoon_season')
        
        # Cap at reasonable maximum
        risk_score = min(0.8, risk_score)
        
        # Determine primary disease from actual reports
        disease_scores = {
            'diarrhea': features['diarrhea_cases'],
            'cholera': features['cholera_cases'],
            'typhoid': features['typhoid_cases']
        }
        primary_disease = max(disease_scores, key=disease_scores.get) if any(disease_scores.values()) else 'diarrhea'
        
        # Predict cases based on current reports and risk
        predicted_cases = max(1, int(features['total_reports'] * (1 + risk_score)))
        
        # Confidence based on data availability
        confidence = 0.5
        if len(health_reports) > 0:
            confidence += 0.2
        if len(water_reports) > 0:
            confidence += 0.2
        if features['total_reports'] > 2:
            confidence += 0.1
        
        return {
            'disease': primary_disease,
            'risk_score': float(risk_score),
            'predicted_cases': predicted_cases,
            'factors': risk_factors,
            'confidence': min(0.95, confidence)
        }

    def save_models(self):
        # No models to save in rule-based system
        pass

    def load_models(self):
        # No models to load in rule-based system
        self.is_trained = True

# Global instance
predictor = OutbreakPredictor()

def predict_outbreak(health_reports, water_reports, location):
    try:
        from services.alert_system import alert_system
        
        prediction = predictor.predict_outbreak(health_reports, water_reports, location)
        alert_result = alert_system.analyze_and_alert(prediction, location)
        
        prediction['alert_generated'] = alert_result.get('alert_needed', False)
        prediction['alert_data'] = alert_result.get('alert_data', {})
        prediction['recipients'] = alert_result.get('recipients', [])
        
        return prediction
    except Exception as e:
        prediction = predictor.predict_outbreak(health_reports, water_reports, location)
        prediction['alert_generated'] = False
        prediction['alert_data'] = {}
        prediction['recipients'] = []
        return prediction