from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class Favorite(SQLModel, table=True):
    property_id: int = Field(foreign_key="property.id", primary_key=True)
    user_id: int = Field(foreign_key="user.id", primary_key=True)

    property: "Property" = Relationship(back_populates="favorites")
    user: "User" = Relationship(back_populates="favorites")