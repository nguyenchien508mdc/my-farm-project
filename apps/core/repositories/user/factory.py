# apps/core/repositories/user/factory.py

from django.conf import settings
from apps.core.repositories.user.base import AbstractUserRepository

def get_user_repository() -> AbstractUserRepository:
    db_type = getattr(settings, "DB_TYPE", "postgres").strip().lower()
    if db_type == "mongo":
        from apps.core.repositories.user.mongo import MongoUserRepository
        return MongoUserRepository()
    elif db_type == "sqlite":
        from apps.core.repositories.user.sqlite import SqliteUserRepository
        return SqliteUserRepository()
    else:
        from apps.core.repositories.user.postgres import PostgresUserRepository
        return PostgresUserRepository()
