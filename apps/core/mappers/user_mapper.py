# apps/core/mappers/user_mapper.py
from apps.core.models import User
from apps.core.schemas.user import UserSchema
from apps.farm.mappers.farm_mapper import  farm_to_schema

def user_to_schema(user: User) -> UserSchema:
    farms = [farm_to_schema(f) for f in user.farms.all()]
    current_farm = farm_to_schema(user.current_farm) if user.current_farm else None

    return UserSchema(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        address=user.address,
        is_verified=user.is_verified,
        date_of_birth=user.date_of_birth,
        profile_picture=user.profile_picture.url if user.profile_picture else None,
        role=user.role,
        role_display=user.get_role_display(),
        farms=farms,
        current_farm=current_farm,
        date_joined=user.date_joined,
        last_login=user.last_login
    )
