from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Note(BaseModel):
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

class ShowNote(Note):
    title: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
