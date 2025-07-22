# apps/core/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from apps.farm.schemas.farm import FarmOutSchema


class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    is_verified: bool
    date_of_birth: Optional[datetime]
    profile_picture: Optional[str]
    role: str
    role_display: str
    farms: List[FarmOutSchema]
    current_farm: Optional[FarmOutSchema]
    date_joined: datetime
    last_login: Optional[datetime]


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password1: str
    new_password2: str
