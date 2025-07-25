# apps/core/mappers/user_mapper.py
from typing import Any, Union
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from apps.core.schemas.user_schema import UserSchema, UserCreateSchema, UserUpdateSchema
from apps.farm.mappers.farm_mapper import farm_to_schema
from django.utils import timezone
from pydantic import ValidationError

User = get_user_model()

def safe_get(obj, attr, default=None):
    """Trả về thuộc tính từ dict hoặc object, fallback về default."""
    return obj.get(attr, default) if isinstance(obj, dict) else getattr(obj, attr, default)

def user_to_schema(user: Any) -> UserSchema:
    farms_raw = safe_get(user, "farms", [])
    farms = [farm_to_schema(farm) for farm in farms_raw.all()] if callable(farms_raw) else [
        farm_to_schema(farm) for farm in farms_raw
    ]

    current_farm = safe_get(user, "current_farm")
    current_farm_schema = farm_to_schema(current_farm) if current_farm else None

    profile_picture_obj = safe_get(user, "profile_picture")
    
    if profile_picture_obj:
        if hasattr(profile_picture_obj, "url") and hasattr(profile_picture_obj, "name"):
            profile_picture = profile_picture_obj.url if profile_picture_obj.name else ""
        elif isinstance(profile_picture_obj, str):
            profile_picture = profile_picture_obj
        else:
            profile_picture = ""
    else:
        profile_picture = ""

    role_display = (
        user.get_role_display() if callable(getattr(user, "get_role_display", None))
        else safe_get(user, "role_display", "")
    )

    return UserSchema(
        id=safe_get(user, "id"),
        username=safe_get(user, "username"),
        email=safe_get(user, "email"),
        first_name=safe_get(user, "first_name", ""),
        last_name=safe_get(user, "last_name", ""),
        phone_number=safe_get(user, "phone_number"),
        address=safe_get(user, "address"),
        is_verified=bool(safe_get(user, "is_verified", False)),
        date_of_birth=safe_get(user, "date_of_birth"),
        profile_picture=profile_picture,
        role=safe_get(user, "role", ""),
        role_display=role_display,
        farms=farms,
        current_farm=current_farm_schema,
        date_joined=safe_get(user, "date_joined"),
        last_login=safe_get(user, "last_login"),
        is_superuser=bool(safe_get(user, "is_superuser", False)),
    )


def create_user_from_schema(schema: UserCreateSchema) -> User:
    """Khởi tạo instance User từ Pydantic schema (chưa lưu vào DB)."""
    profile_picture = getattr(schema, "profile_picture", None)

    user = User(
        username=schema.username,
        email=schema.email,
        first_name=schema.first_name or "",
        last_name=schema.last_name or "",
        password=make_password(schema.password),
        date_joined=timezone.now(),
        is_verified=False,
        role="user",
    )
    if profile_picture:
        user.profile_picture = profile_picture 

    return user

def update_user_from_schema(user: User, raw_data: Union[dict, UserUpdateSchema]) -> User:
    """
    Cập nhật user từ dict hoặc schema (không lưu vào DB).
    Tự động flatten nếu là dict.
    """

    if isinstance(raw_data, dict):
        # Flatten list 1 phần tử -> giá trị đơn
        flattened = {
            k: v[0] if isinstance(v, list) and len(v) == 1 else v
            for k, v in raw_data.items()
        }

        try:
            schema = UserUpdateSchema.model_validate(flattened)
        except ValidationError as e:
            raise e
    elif isinstance(raw_data, UserUpdateSchema):
        schema = raw_data
    else:
        raise TypeError("raw_data phải là dict hoặc UserUpdateSchema")

    update_data = schema.model_dump(exclude_unset=True)

    profile_picture = update_data.pop("profile_picture", None)
    if profile_picture is not None:
        user.profile_picture = profile_picture

    for key, value in update_data.items():
        setattr(user, key, value)

    return user