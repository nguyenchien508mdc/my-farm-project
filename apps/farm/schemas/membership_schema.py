# apps/farm/schemas/membership_schema.py
from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, constr

from apps.core.schemas.user_schema import UserSchema
from apps.farm.schemas.farm_schema import FarmOutSchema

class FarmMembershipSchema(BaseModel):
    role: constr(min_length=1, max_length=50)
    joined_date: Optional[date] = None
    is_active: bool = True
    can_approve: bool = False

class FarmMembershipCreateUpdateSchema(FarmMembershipSchema):
    farm_id: int
    user_id: int

class FarmMembershipOutSchema(FarmMembershipSchema):
    id: int
    farm: FarmOutSchema
    user: UserSchema
    role_display: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
