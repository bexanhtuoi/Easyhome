from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship

class Province(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    district_rel: List["District"] = Relationship(back_populates="province_rel")
    users: List["User"] = Relationship(back_populates="province_rel")
    properties: List["Property"] = Relationship(back_populates="province")