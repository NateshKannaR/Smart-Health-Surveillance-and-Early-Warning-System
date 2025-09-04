from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WaterQualityCreate(BaseModel):
    location: str
    ph_level: float
    turbidity: float
    bacterial_count: int
    chlorine_level: float
    temperature: float
    tested_by: int
    source_type: str

class WaterQualityResponse(BaseModel):
    id: int
    location: str
    ph_level: float
    turbidity: float
    bacterial_count: int
    chlorine_level: float
    temperature: float
    tested_at: datetime
    tested_by: int
    source_type: str
    is_contaminated: bool
    
    class Config:
        from_attributes = True