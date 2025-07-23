# apps/core/mappers/user_mapper.py
from typing import Any
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from apps.core.schemas.user_schema import UserSchema, UserCreateSchema, UserUpdateSchema
from apps.farm.mappers.farm_mapper import farm_to_schema
import datetime

User = get_user_model()


def user_to_schema(user: Any) -> UserSchema:
    get = lambda obj, attr, default=None: getattr(obj, attr, default) if not isinstance(obj, dict) else obj.get(attr, default)

    farms_raw = get(user, "farms", [])
    if callable(farms_raw):  # Django ORM related manager
        farms = [farm_to_schema(farm) for farm in farms_raw.all()]
    else:
        farms = [farm_to_schema(farm) for farm in farms_raw]

    current_farm = get(user, "current_farm")
    if current_farm:
        current_farm = farm_to_schema(current_farm)

    profile_picture = get(user, "profile_picture")
    if profile_picture and hasattr(profile_picture, "url"):
        profile_picture = profile_picture.url
    else:
        profile_picture = ""

    role_display = get(user, "get_role_display")
    if callable(role_display):
        role_display = role_display()
    else:
        role_display = get(user, "role_display", "")

    schema = UserSchema(
        id=get(user, "id"),
        username=get(user, "username"),
        email=get(user, "email"),
        first_name=get(user, "first_name", ""),
        last_name=get(user, "last_name", ""),
        phone_number=get(user, "phone_number"),
        address=get(user, "address"),
        is_verified=get(user, "is_verified", False),
        date_of_birth=get(user, "date_of_birth"),
        profile_picture=profile_picture,
        role=get(user, "role", ""),
        role_display=role_display,
        farms=farms,
        current_farm=current_farm,
        date_joined=get(user, "date_joined"),
        last_login=get(user, "last_login"),
    )
    return schema

def create_user_from_schema(schema: UserCreateSchema) -> User:
    user = User(
        username=schema.username,
        email=schema.email,
        first_name=schema.first_name or "",
        last_name=schema.last_name or "",
        password=make_password(schema.password),
        date_joined=datetime.datetime.utcnow(),
        is_verified=False,
        role="user",
    )
    return user

def update_user_from_schema(user: User, schema: UserUpdateSchema) -> User:
    update_data = schema.model_dump(exclude_unset=True)  
    for key, value in update_data.items():
        setattr(user, key, value)
    return user
