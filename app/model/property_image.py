from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class PropertyImages(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    property_id: int = Field(foreign_key="property.id")
    image_url: str
    is_thumbnail: bool = False

    property: Property = Relationship(back_populates="images")