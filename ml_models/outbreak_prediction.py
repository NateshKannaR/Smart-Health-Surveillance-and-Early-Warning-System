import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, mean_squared_error
)
import joblib
from datetime import datetime
from xgboost import XGBClassifier, XGBRegressor

class OutbreakPredictor:
    def __init__(self):
        self.disease_classifier = XGBClassifier(n_estimators=100, random_state=42)
        self.case_predictor = XGBRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False

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
        avg_ph = np.mean([w.get('ph_level', 7.0) for w in water_reports])
        avg_turbidity = np.mean([w.get('turbidity', 0) for w in water_reports])
        avg_bacterial = np.mean([w.get('bacterial_count', 0) for w in water_reports])

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
        if not training_data:
            training_data = self._generate_synthetic_data()

        df = pd.DataFrame(training_data)
        feature_columns = [
            'total_reports', 'diarrhea_cases', 'cholera_cases', 'typhoid_cases',
            'severe_cases', 'moderate_cases', 'vulnerable_age_cases',
            'contaminated_sources', 'contamination_rate', 'avg_ph_deviation',
            'avg_turbidity', 'avg_bacterial_count', 'is_monsoon', 'is_winter',
            'month', 'population_density'
        ]

        X = df[feature_columns]
        y_outbreak = df['outbreak_occurred']
        y_cases = df['future_cases']

        X_train, X_test, y_train, y_test = train_test_split(X, y_outbreak, test_size=0.2, random_state=42)
        X_cases_train, X_cases_test, y_cases_train, y_cases_test = train_test_split(X, y_cases, test_size=0.2, random_state=42)

        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        X_cases_train_scaled = self.scaler.transform(X_cases_train)
        X_cases_test_scaled = self.scaler.transform(X_cases_test)

        self.disease_classifier.fit(X_train_scaled, y_train)
        self.case_predictor.fit(X_cases_train_scaled, y_cases_train)
        self.is_trained = True
        self.save_models()

        return {"status": "trained"}

    def predict_outbreak(self, health_reports, water_reports, location):
        if not self.is_trained:
            self.load_models()

        if isinstance(location, str):
            location_data = {'population_density': 500}
        else:
            location_data = location

        features = self.prepare_features(health_reports, water_reports, location_data)
        feature_array = np.array([list(features.values())])
        feature_array_scaled = self.scaler.transform(feature_array)

        outbreak_prob = self.disease_classifier.predict_proba(feature_array_scaled)[0][1]
        predicted_cases = max(0, int(self.case_predictor.predict(feature_array_scaled)[0]))

        disease_scores = {
            'diarrhea': features['diarrhea_cases'],
            'cholera': features['cholera_cases'],
            'typhoid': features['typhoid_cases']
        }
        primary_disease = max(disease_scores, key=disease_scores.get) if any(disease_scores.values()) else 'diarrhea'

        risk_factors = []
        if features['contamination_rate'] > 0.3:
            risk_factors.append('high_water_contamination')
        if features['severe_cases'] > 3:
            risk_factors.append('severe_cases_present')
        if features['is_monsoon']:
            risk_factors.append('monsoon_season')
        if features['vulnerable_age_cases'] > 2:
            risk_factors.append('vulnerable_population_affected')

        return {
            'disease': primary_disease,
            'risk_score': float(outbreak_prob),
            'predicted_cases': predicted_cases,
            'factors': risk_factors,
            'confidence': min(0.95, 0.5 + (len(health_reports) * 0.02) + (len(water_reports) * 0.01))
        }

    def _generate_synthetic_data(self, n=100):
        np.random.seed(42)
        data = []
        for _ in range(n):
            total_reports = np.random.poisson(5)
            contamination_rate = np.random.beta(2, 5)
            is_monsoon = np.random.choice([0, 1], p=[0.7, 0.3])
            outbreak_prob = 0.1 + (total_reports * 0.05) + (contamination_rate * 0.4) + (is_monsoon * 0.2)
            outbreak_occurred = 1 if np.random.random() < outbreak_prob else 0
            future_cases = max(0, int(np.random.normal(total_reports * 1.5, 2)))

            data.append({
                'total_reports': total_reports,
                'diarrhea_cases': np.random.poisson(2),
                'cholera_cases': np.random.poisson(1),
                'typhoid_cases': np.random.poisson(1),
                'severe_cases': np.random.poisson(1),
                'moderate_cases': np.random.poisson(2),
                'vulnerable_age_cases': np.random.poisson(2),
                'contaminated_sources': int(contamination_rate * 10),
                'contamination_rate': contamination_rate,
                'avg_ph_deviation': np.random.exponential(0.5),
                'avg_turbidity': np.random.exponential(2),
                'avg_bacterial_count': np.random.poisson(5),
                'is_monsoon': is_monsoon,
                'is_winter': np.random.choice([0, 1], p=[0.8, 0.2]),
                'month': np.random.randint(1, 13),
                'population_density': np.random.normal(500, 200),
                'outbreak_occurred': outbreak_occurred,
                'future_cases': future_cases
            })
        return data

    def save_models(self):
        try:
            joblib.dump(self.disease_classifier, 'outbreak_classifier.pkl')
            joblib.dump(self.case_predictor, 'case_predictor.pkl')
            joblib.dump(self.scaler, 'feature_scaler.pkl')
        except:
            pass

    def load_models(self):
        try:
            self.disease_classifier = joblib.load('outbreak_classifier.pkl')
            self.case_predictor = joblib.load('case_predictor.pkl')
            self.scaler = joblib.load('feature_scaler.pkl')
            self.is_trained = True
        except:
            self.train_model()

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