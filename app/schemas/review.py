from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewCreateSchema(BaseModel):
    property_id: int
    rating: Optional[int] = None
    comment: Optional[str] = None

class ReviewUpdateSchema(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None
    update_at: Optional[datetime] = None
