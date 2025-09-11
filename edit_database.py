from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.main import HealthReport, WaterSource, Alert, Base

# Database connection
engine = create_engine("sqlite:///./health_surveillance.db")
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# Example: Add new health report
new_report = HealthReport(
    disease="Cholera",
    severity="severe", 
    location="Village B"
)
db.add(new_report)
db.commit()

# Example: Update existing record
report = db.query(HealthReport).filter(HealthReport.id == 1).first()
if report:
    report.severity = "mild"
    db.commit()

# Example: View all records
reports = db.query(HealthReport).all()
for r in reports:
    print(f"ID: {r.id}, Disease: {r.disease}, Severity: {r.severity}")

db.close()