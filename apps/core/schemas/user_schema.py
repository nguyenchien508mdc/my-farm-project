# apps/core/schemas/user_schema.py
from pydantic import BaseModel, EmailStr, validator, Field, model_validator
from typing import Optional, List
from datetime import date, datetime
from apps.farm.schemas.farm_schema import FarmOutSchema


class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    is_verified: bool
    date_of_birth: Optional[date]
    profile_picture: Optional[str] = None
    role: str
    role_display: str
    farms: List[FarmOutSchema]
    current_farm: Optional[FarmOutSchema]
    date_joined: Optional[datetime] = None
    last_login: Optional[datetime]
    is_superuser: Optional[bool] = False


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: Optional[str] = Field(None, alias="password2")  
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @model_validator(mode='after')
    def check_password_match(cls, model):
        if model.password != model.confirm_password:
            raise ValueError("Password confirmation does not match.")
        return model

    class Config:
        extra = "ignore"
        allow_population_by_field_name = True


class UserUpdateSchema(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[date] = Field(None, example="2003-08-05")

    @validator("phone_number")
    def phone_number_must_be_digits(cls, v):
        if v and not v.isdigit():
            raise ValueError("phone_number must contain digits only")
        return v

    class Config:
        extra = "ignore"

class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password1: str
    new_password2: str

