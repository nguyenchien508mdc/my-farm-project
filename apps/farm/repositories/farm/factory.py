# apps\farm\repositories\farm\factory.py

from django.conf import settings
from apps.farm.repositories.farm.base import AbstractFarmRepository

def get_farm_repository() -> AbstractFarmRepository:
    db_type = getattr(settings, "DB_TYPE", "postgres").strip().lower()
    if db_type == "mongo":
        from apps.farm.repositories.farm.mongo import MongoFarmRepository
        return MongoFarmRepository()
    elif db_type == "sqlite":
        from apps.farm.repositories.farm.sqlite import SqliteFarmRepository
        return SqliteFarmRepository()
    else:
        from apps.farm.repositories.farm.postgres import PostgresFarmRepository
        return PostgresFarmRepository()