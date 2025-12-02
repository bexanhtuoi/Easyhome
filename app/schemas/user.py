from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.model.user import GenderEnum

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBaseSchema(BaseModel):
    full_name: str
    email: str

class UserCreateSchema(UserBaseSchema):
    password: str

class UserUpdateSchema(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None
    gender: Optional[GenderEnum] = None
    birthday: Optional[datetime] = None
    cccd_id: Optional[str] = None
    province: Optional[int] = None
    district: Optional[int] = None
    ward: Optional[int] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    zalo: Optional[str] = None
    is_verified: Optional[bool] = None
    update_at: Optional[datetime] = None
