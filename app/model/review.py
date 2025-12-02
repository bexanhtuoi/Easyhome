from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    property_id: int = Field(foreign_key="property.id")
    user_id: int = Field(foreign_key="user.id")
    rating: Optional[int] = None
    comment: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    property: "Property" = Relationship(back_populates="reviews")
    user: "User" = Relationship(back_populates="reviews")