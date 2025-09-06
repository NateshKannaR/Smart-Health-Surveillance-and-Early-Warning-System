import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.main import HealthReport, WaterSource, Alert, Base

# Database connection
engine = create_engine("sqlite:///../health_surveillance.db")
SessionLocal = sessionmaker(bind=engine)

# Create tables first
Base.metadata.create_all(bind=engine)
print("Database tables created/verified")

db = SessionLocal()

print("=== Health Surveillance Database Editor ===")

# Add sample data
print("Adding sample data...")

# Add health reports
reports_data = [
    {"disease": "Diarrhea", "severity": "mild", "location": "Village A"},
    {"disease": "Cholera", "severity": "severe", "location": "Village B"},
    {"disease": "Typhoid", "severity": "moderate", "location": "Village C"}
]

for data in reports_data:
    report = HealthReport(**data)
    db.add(report)

# Add water sources
sources_data = [
    {"is_safe": True, "ph_level": 7.2, "turbidity": 2.1, "bacterial_count": 5, "temperature": 24.5, "source_type": "well"},
    {"is_safe": False, "ph_level": 6.1, "turbidity": 15.8, "bacterial_count": 180, "temperature": 26.3, "source_type": "river"}
]

for data in sources_data:
    source = WaterSource(**data)
    db.add(source)

# Add alerts
alerts_data = [
    {"severity": "high", "is_active": True},
    {"severity": "medium", "is_active": True}
]

for data in alerts_data:
    alert = Alert(**data)
    db.add(alert)

db.commit()

# Display current data
print("\n--- Health Reports ---")
reports = db.query(HealthReport).all()
for r in reports:
    print(f"ID: {r.id}, Disease: {r.disease}, Severity: {r.severity}, Location: {r.location}")

print("\n--- Water Sources ---")
sources = db.query(WaterSource).all()
for s in sources:
    print(f"ID: {s.id}, Safe: {s.is_safe}, pH: {s.ph_level}, Type: {s.source_type}")

print("\n--- Alerts ---")
alerts = db.query(Alert).all()
for a in alerts:
    print(f"ID: {a.id}, Severity: {a.severity}, Active: {a.is_active}")

print("\nDatabase setup complete!")
db.close()