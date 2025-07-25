# apps/core/repositories/user/postgres.py

from apps.core.models import User
from apps.core.schemas.user_schema import UserCreateSchema, UserUpdateSchema
from typing import Optional, List, Union
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.contrib.auth.hashers import check_password, make_password
from django.utils.timezone import now
import uuid
import os

class PostgresUserRepository:
    def create_user(self, data: UserCreateSchema) -> dict:
        user = User.objects.create_user(
            username=data.username,
            email=data.email,
            password=data.password,
            first_name=data.first_name or "",
            last_name=data.last_name or "",
        )
        return self._to_dict(user)

    def get_by_id(self, user_id: Union[int, str]) -> Optional[dict]:
        try:
            user = User.objects.get(id=user_id)
            return self._to_dict(user)
        except User.DoesNotExist:
            return None

    def get_by_username(self, username: str) -> Optional[dict]:
        user = User.objects.filter(username=username).first()
        return self._to_dict(user) if user else None

    def get_by_email(self, email: str) -> Optional[dict]:
        user = User.objects.filter(email=email).first()
        return self._to_dict(user) if user else None

    def update_user(self, user_id: Union[int, str], data: UserUpdateSchema) -> dict:
        user = User.objects.get(id=user_id)
        for field, value in data.dict(exclude_unset=True).items():
            if field == "profile_picture" and value:
                # Nếu là file
                if hasattr(value, "read") and hasattr(value, "name"):
                    ext = os.path.splitext(value.name)[-1] or ".jpg"
                    filename = f"{uuid.uuid4().hex}{ext}"
                    upload_path = os.path.join("user_profiles", filename)
                    with open(os.path.join("media", upload_path), "wb") as f:
                        f.write(value.read())
                    user.profile_picture = upload_path
                elif isinstance(value, str):
                    user.profile_picture = value.lstrip("/media/")
            else:
                setattr(user, field, value)
        user.save()
        return self._to_dict(user)

    def delete_user(self, user_id: Union[int, str]) -> bool:
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return True
        except User.DoesNotExist:
            return False

    def change_password(self, user_id: Union[int, str], new_password: str) -> bool:
        try:
            user = User.objects.get(id=user_id)
            user.password = make_password(new_password)
            user.save()
            return True
        except User.DoesNotExist:
            return False

    def get_password_hash(self, user_id: Union[int, str]) -> Optional[str]:
        try:
            user = User.objects.get(id=user_id)
            return user.password
        except User.DoesNotExist:
            return None

    def list_users(self) -> List[dict]:
        return [self._to_dict(user) for user in User.objects.all()]

    def list_free_users(self, farm_id: Union[int, str]) -> List[dict]:
        from apps.farm.models import FarmMembership
        used_user_ids = FarmMembership.objects.filter(farm_id=farm_id).values_list("user_id", flat=True)
        free_users = User.objects.exclude(id__in=used_user_ids)
        return [self._to_dict(user) for user in free_users]

    def initiate_password_reset(self, email: str) -> bool:
        try:
            user = User.objects.get(email=email)
            print(f"Password reset requested for: {email}")
            return True
        except User.DoesNotExist:
            return False

    def confirm_password_reset(self, token: str, new_password: str) -> bool:
        return False

    def save_password_reset_token(self, user_id: int, token: str) -> None:
        pass

    def _to_dict(self, user: User) -> dict:
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone_number": user.phone_number,
            "address": user.address,
            "date_of_birth": user.date_of_birth,
            "date_joined": user.date_joined,
            "last_login": user.last_login,
            "is_verified": user.is_verified,
            "role": user.role,
            "role_display": user.get_role_display(),
            "profile_picture": f"/media/{user.profile_picture}" if user.profile_picture else "",
            "farms": [],  
            "current_farm": user.current_farm_id,
        }

