from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from app.model.link_model import Property_Nearby_Place

class NearbyPlace(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    properties: List["Property"] = Relationship(back_populates="nearby_places", link_model=Property_Nearby_Place)

