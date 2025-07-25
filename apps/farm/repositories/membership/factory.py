from django.conf import settings
from apps.farm.repositories.membership.base import AbstractFarmMembershipRepository


def get_membership_repository() -> AbstractFarmMembershipRepository:
    db_type = getattr(settings, "DB_TYPE", "postgres").strip().lower()

    if db_type == "sqlite":
        from apps.farm.repositories.membership.sqlite import SqliteFarmMembershipRepository
        return SqliteFarmMembershipRepository()
    elif db_type == "postgres":
        from apps.farm.repositories.membership.postgres import PostgresFarmMembershipRepository
        return PostgresFarmMembershipRepository()
    elif db_type == "mongo":
        from apps.farm.repositories.membership.mongo import MongoFarmMembershipRepository
        return MongoFarmMembershipRepository()
    else:
        raise ValueError(f"Unsupported DB_TYPE: {db_type}")
