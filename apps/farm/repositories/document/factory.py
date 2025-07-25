# apps/farm/repositories/document/factory.py
from django.conf import settings
from apps.farm.repositories.document.base import AbstractFarmDocumentRepository

def get_document_repository() -> AbstractFarmDocumentRepository:
    db_type = getattr(settings, "DB_TYPE", "postgres").strip().lower()

    if db_type == "mongo":
        from apps.farm.repositories.document.mongo import MongoDocumentRepository
        return MongoDocumentRepository()
    elif db_type == "sqlite":
        from apps.farm.repositories.document.sqlite import SqliteDocumentRepository
        return SqliteDocumentRepository()
    elif db_type == "postgres":
        from apps.farm.repositories.document.postgres import PostgresDocumentRepository
        return PostgresDocumentRepository()
    else:
        raise ValueError(f"Unsupported DB_TYPE '{db_type}' in settings")
