from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr
from enum import Enum


class GenderEnum(str, Enum):
    male = "male"
    female = "female"


class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"
    moderator = "moderator"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email: EmailStr = Field(unique=True, index=True)
    password_hashed: Optional[str]
    avatar: Optional[str] = None
    gender: Optional[GenderEnum] = None
    birthday: Optional[datetime] = None
    cccd_id: Optional[str] = Field(unique=True, index=True)
    province: Optional[int] = Field(default=None, foreign_key="province.id")
    district: Optional[int] = Field(default=None, foreign_key="district.id")
    ward: Optional[int] = Field(default=None, foreign_key="ward.id")
    address: Optional[str] = None
    phone: Optional[str] = None
    zalo: Optional[str] = None
    role: Optional[RoleEnum] = Field(default=RoleEnum.user)
    super_user: bool = Field(default=False, nullable=False)
    is_verified: bool = Field(default=False, nullable=False)

    create_at: datetime = Field(default_factory=datetime.utcnow)
    update_at: datetime = Field(default_factory=datetime.utcnow)

    province_rel: Optional["Province"] = Relationship(back_populates="users")
    district_rel: Optional["District"] = Relationship(back_populates="users")
    ward_rel: Optional["Ward"] = Relationship(back_populates="users")
    properties: List["Property"] = Relationship(back_populates="owner")
    favorites: List["Favorite"] = Relationship(back_populates="user")
    reviews: List["Review"] = Relationship(back_populates="user")