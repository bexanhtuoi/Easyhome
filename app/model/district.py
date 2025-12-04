from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship
from app.model.province import Province

class District(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    province_id: int = Field(foreign_key="province.id")

    province_rel: Optional["Province"] = Relationship(back_populates="district_rel")
    users: List["User"] = Relationship(back_populates="district_rel")
    ward_rel: List["Ward"] = Relationship(back_populates="district_rel")
    properties: List["Property"] = Relationship(back_populates="district_rel")
    