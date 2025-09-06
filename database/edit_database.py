import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.main import HealthReport, WaterSource, Alert

# Database connection
engine = create_engine("sqlite:///../health_surveillance.db")
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

print("=== Health Surveillance Database Editor ===")

# View existing data
print("\n--- Current Health Reports ---")
reports = db.query(HealthReport).all()
for r in reports:
    print(f"ID: {r.id}, Disease: {r.disease}, Severity: {r.severity}, Location: {r.location}")

print("\n--- Current Water Sources ---")
sources = db.query(WaterSource).all()
for s in sources:
    print(f"ID: {s.id}, Safe: {s.is_safe}, pH: {s.ph_level}, Type: {s.source_type}")

print("\n--- Current Alerts ---")
alerts = db.query(Alert).all()
for a in alerts:
    print(f"ID: {a.id}, Severity: {a.severity}, Active: {a.is_active}")

# Example: Add new records
print("\n--- Adding Sample Data ---")

# Add health report
new_report = HealthReport(
    disease="Cholera",
    severity="severe", 
    location="Village B"
)
db.add(new_report)

# Add water source
new_source = WaterSource(
    is_safe=False,
    ph_level=6.2,
    turbidity=18.5,
    bacterial_count=200,
    temperature=26.0,
    source_type="river"
)
db.add(new_source)

db.commit()
print("Sample data added successfully!")

db.close()