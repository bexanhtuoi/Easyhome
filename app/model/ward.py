from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship

class Ward(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    district_id: int = Field(foreign_key="district.id")

    district_rel: Optional["District"] = Relationship(back_populates="ward_rel")
    users: List["User"] = Relationship(back_populates="ward_rel")
    # properties: List["Property"] = Relationship(back_populates="ward_rel")