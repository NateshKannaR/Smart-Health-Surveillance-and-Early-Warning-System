from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AlertCreate(BaseModel):
    alert_type: str
    location: str
    message: str
    severity: str
    affected_population: Optional[int] = 0

class AlertResponse(BaseModel):
    id: int
    alert_type: str
    location: str
    message: str
    severity: str
    created_at: datetime
    is_resolved: bool
    affected_population: Optional[int]
    
    class Config:
        from_attributes = True