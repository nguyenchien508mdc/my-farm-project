# apps/farm/schemas/farm.py
from pydantic import BaseModel, validator, Field, constr
from typing import Optional, Any
from datetime import date, datetime

class FarmCreateUpdateSchema(BaseModel):
    name: constr(min_length=1, max_length=255)
    location: Optional[str] = None
    area: float = Field(..., ge=0, description="Diện tích không thể âm")
    farm_type: constr(min_length=1, max_length=100)
    description: Optional[str] = None
    is_active: bool = True
    established_date: Optional[date] = None
    logo: Optional[Any] = None 

    @validator('area')
    def area_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError("Diện tích không thể âm")
        return v

class FarmPartialUpdateSchema(BaseModel):
    name: Optional[constr(min_length=1, max_length=255)]
    location: Optional[str]
    area: Optional[float] = Field(None, ge=0, description="Diện tích không thể âm")
    farm_type: Optional[constr(min_length=1, max_length=100)]
    description: Optional[str]
    is_active: Optional[bool]
    established_date: Optional[date]
    logo: Optional[Any] = None

    @validator('area')
    def area_must_be_non_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError("Diện tích không thể âm")
        return v
    class Config:
        extra = "allow"

class FarmOutSchema(FarmCreateUpdateSchema):
    id: int
    slug: constr(min_length=1, max_length=255) 
    farm_type_display: Optional[str] = None
    members_count: int = 0
    active_members_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
