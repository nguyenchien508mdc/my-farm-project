# apps/core/repositories/user/postgres.py

from apps.core.models import User
from apps.core.schemas.user_schema import UserCreateSchema
from typing import Optional

class PostgresUserRepository:
    def create_user(self, data: UserCreateSchema) -> User:
        return User.objects.create_user(
            username=data.username,
            email=data.email,
            password=data.password,
            first_name=data.first_name or "",
            last_name=data.last_name or "",
        )

    def get_by_username(self, username: str) -> Optional[User]:
        return User.objects.filter(username=username).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return User.objects.filter(email=email).first()

    def get_by_id(self, user_id: int) -> Optional[User]:
        return User.objects.filter(id=user_id).first()
