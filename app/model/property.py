# from typing import Optional, List
# from sqlmodel import Field, SQLModel, Relationship
# from datetime import datetime

# class Property(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     owner_id: int = Field(foreign_key="user.user_id")
#     title: str
#     description: Optional[str] = None
#     rule_text: Optional[str] = None
#     category_id: Optional[int] = Field(default=None, foreign_key="category.id")
#     price: Optional[float] = None
#     rooms_count: Optional[int] = None
#     area: Optional[float] = None
#     province: Optional[int] = Field(default=None, foreign_key="province.id")
#     district: Optional[int] = Field(default=None, foreign_key="district.id")
#     ward: Optional[int] = Field(default=None, foreign_key="ward.id")
#     address: Optional[str] = None
#     owner_phone: Optional[str] = None
#     owner_zalo: Optional[str] = None
#     owner_name: Optional[str] = None
#     latitude: Optional[float] = None
#     longitude: Optional[float] = None
#     status: Optional[str] = None
#     create_at: datetime = Field(default_factory=datetime.utcnow)
#     update_at: datetime = Field(default_factory=datetime.utcnow)

#     owner: "User" = Relationship(back_populates="properties")
#     category: Optional["Category"] = Relationship(back_populates="properties")
#     images: List["PropertyImages"] = Relationship(back_populates="property")
#     amenities: List["Amenities"] = Relationship(back_populates="properties", link_model="Property_Amenities")
#     objects: List["Object"] = Relationship(back_populates="properties", link_model="Property_Object")
#     nearby_places: List["NearbyPlace"] = Relationship(back_populates="properties", link_model="Property_Nearby_Place")
#     favorites: List["Favorite"] = Relationship(back_populates="property")
#     reviews: List["Review"] = Relationship(back_populates="property")