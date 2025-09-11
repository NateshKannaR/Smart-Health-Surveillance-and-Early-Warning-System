from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    phone: str
    role: str
    location: str
    language_preference: Optional[str] = "en"

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    phone: str
    role: str
    location: str
    language_preference: str
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True