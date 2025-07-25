# apps/core/services/user_service.py
from typing import Optional, List
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password

from apps.core.schemas.user_schema import (
    UserCreateSchema,
    UserSchema,
    ChangePasswordSchema,
    UserUpdateSchema,
)
from apps.core.mappers.user_mapper import user_to_schema
from apps.core.repositories.user.factory import get_user_repository

user_repo = get_user_repository()


class UserService:

    async def generate_password_reset_link(self, user, request) -> str:
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        from django.urls import reverse
        import uuid

        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        token = str(uuid.uuid4())  # hoặc dùng repo method để tạo token và lưu DB

        # Giả sử bạn có method lưu token vào DB trong repo
        await user_repo.save_password_reset_token(user.id, token)

        reset_url = request.build_absolute_uri(
            reverse("core:password_reset_confirm", kwargs={"uidb64": uidb64, "token": token})
        )
        return reset_url

    async def create_user(self, data: UserCreateSchema) -> UserSchema:
        hashed_data = data.copy(update={"password": make_password(data.password)})
        user_dict = await user_repo.create_user(hashed_data)
        return user_to_schema(user_dict)

    async def get_user_by_username(self, username: str) -> Optional[UserSchema]:
        user = await user_repo.get_by_username(username)
        return user_to_schema(user) if user else None

    async def get_by_email(self, email: str) -> Optional[UserSchema]:
        user = await user_repo.get_by_email(email)
        return user_to_schema(user) if user else None

    async def get_by_id(self, user_id: int) -> Optional[UserSchema]:
        user = await user_repo.get_by_id(user_id)
        return user_to_schema(user) if user else None

    async def list_users(self) -> List[UserSchema]:
        users = await user_repo.list_users()
        return [user_to_schema(user) for user in users]

    async def list_free_users(self, farm_id: int) -> List[UserSchema]:
        users = await user_repo.list_free_users(farm_id)
        return [user_to_schema(user) for user in users]

    async def update_user(self, user_id: int, schema: UserUpdateSchema) -> UserSchema:
        existing_user = await user_repo.get_by_id(user_id)
        if not existing_user:
            raise ValidationError("User không tồn tại")

        updated_user = await user_repo.update_user(user_id, schema)
        return user_to_schema(updated_user)

    async def delete_user(self, user_id: int) -> bool:
        return await user_repo.delete_user(user_id)

    async def change_password(
        self, user_id: int, old_password: str, new_password1: str, new_password2: str
    ) -> bool:
        if new_password1 != new_password2:
            raise ValidationError("Mật khẩu mới không khớp")

        user = await user_repo.get_by_id(user_id)
        if not user:
            raise ValidationError("User không tồn tại")

        password_hash = await user_repo.get_password_hash(user_id)
        if not check_password(old_password, password_hash):
            raise ValidationError("Mật khẩu cũ không đúng")

        validate_password(new_password1)
        new_password_hashed = make_password(new_password1)
        return await user_repo.change_password(user_id, new_password_hashed)

    async def initiate_password_reset(self, email: str) -> bool:
        return await user_repo.initiate_password_reset(email)

    async def confirm_password_reset(self, token: str, new_password: str) -> bool:
        validate_password(new_password)
        hashed = make_password(new_password)
        return await user_repo.confirm_password_reset(token, hashed)
