from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PropertyBaseSchema(BaseModel):
    title: str
    description: Optional[str] = None
    rule_text: Optional[str] = None
    price: float
    address: str
    province_id: int
    district_id: int
    ward_id: int
    category_id: int
    area: Optional[float] = None
    rooms_count: Optional[int] = None
    owner_name: Optional[str] = None
    owner_phone: Optional[str] = None
    owner_zalo: Optional[str] = None
    status: Optional[str] = None
    amenities_id: Optional[List[int]] =None
    objects_id: Optional[List[int]] =None
    nearby_places_id: Optional[List[int]] =None

    latitude: Optional[float] = None
    longitude: Optional[float] = None
    


class PropertyCreateSchema(PropertyBaseSchema):
    owner_id: Optional[int] = None


class PropertyUpdateSchema(PropertyBaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    rule_text: Optional[str] = None
    price: Optional[float] = None
    address: Optional[str] = None
    province_id: Optional[int] = None
    district_id: Optional[int] = None
    ward_id: Optional[int] = None
    category_id: Optional[int] = None

    update_at: Optional[datetime] = None


class PropertyImageRead(BaseModel):
    id: int
    property_id: int
    image_url: str
    is_thumbnail: bool
    

class AmenityRead(BaseModel):
    id: int
    name: str


class ObjectRead(BaseModel):
    id: int
    name: str


class NearbyPlaceRead(BaseModel):
    id: int
    name: str


class PropertyResponseSchema(BaseModel):
    id: int
    owner_id: int
    title: str
    description: Optional[str] = None
    rule_text: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[float] = None
    rooms_count: Optional[int] = None
    area: Optional[float] = None
    province: Optional[int] = None
    district: Optional[int] = None
    ward: Optional[int] = None
    address: Optional[str] = None
    owner_phone: Optional[str] = None
    owner_zalo: Optional[str] = None
    owner_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    status: Optional[str] = None
    create_at: datetime
    update_at: datetime

    images: Optional[List[PropertyImageRead]] = None
    amenities: Optional[List[AmenityRead]] = None
    objects: Optional[List[ObjectRead]] = None
    nearby_places: Optional[List[NearbyPlaceRead]] = None


    