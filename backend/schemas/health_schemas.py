from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class HealthReportCreate(BaseModel):
    reporter_id: int
    patient_age: int
    patient_gender: str
    symptoms: List[str]
    location: str
    severity: str

class HealthReportResponse(BaseModel):
    id: int
    reporter_id: int
    patient_age: int
    patient_gender: str
    symptoms: str
    location: str
    reported_at: datetime
    severity: str
    disease_suspected: Optional[str]
    
    class Config:
        from_attributes = True