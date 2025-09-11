from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from database.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    role = Column(String)  # ASHA, volunteer, health_official, admin
    location = Column(String)
    language_preference = Column(String, default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class HealthReport(Base):
    __tablename__ = "health_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    reporter_id = Column(Integer, ForeignKey("users.id"))
    patient_age = Column(Integer)
    patient_gender = Column(String)
    symptoms = Column(Text)  # JSON string of symptoms
    location = Column(String)
    reported_at = Column(DateTime, default=datetime.utcnow)
    severity = Column(String)  # mild, moderate, severe
    disease_suspected = Column(String)
    
    reporter = relationship("User", back_populates="reports")

class WaterQualityReport(Base):
    __tablename__ = "water_quality_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    ph_level = Column(Float)
    turbidity = Column(Float)
    bacterial_count = Column(Integer)
    chlorine_level = Column(Float)
    temperature = Column(Float)
    tested_at = Column(DateTime, default=datetime.utcnow)
    tested_by = Column(Integer, ForeignKey("users.id"))
    source_type = Column(String)  # well, river, pond, tap
    is_contaminated = Column(Boolean, default=False)

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(String)  # outbreak_warning, water_contamination, resource_needed
    location = Column(String)
    message = Column(Text)
    severity = Column(String)  # low, medium, high, critical
    created_at = Column(DateTime, default=datetime.utcnow)
    is_resolved = Column(Boolean, default=False)
    affected_population = Column(Integer)

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    disease = Column(String)
    risk_score = Column(Float)
    predicted_cases = Column(Integer)
    prediction_date = Column(DateTime, default=datetime.utcnow)
    factors = Column(Text)  # JSON string of contributing factors
    confidence = Column(Float)

User.reports = relationship("HealthReport", back_populates="reporter")