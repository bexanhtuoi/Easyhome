from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from app.model import Property_Object

class Object(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    properties: List["Property"] = Relationship(back_populates="objects", link_model=Property_Object)