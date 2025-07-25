# apps/farm/repositories/document/sqlite.py

from typing import List, Optional
from asgiref.sync import sync_to_async

from apps.farm.repositories.document.base import AbstractFarmDocumentRepository
from apps.farm.schemas.document_schema import FarmDocumentCreateUpdateSchema
from apps.farm.models import FarmDocument

class SqliteDocumentRepository(AbstractFarmDocumentRepository):

    @sync_to_async
    def get(self, pk: int) -> Optional[FarmDocument]:
        try:
            return FarmDocument.objects.get(pk=pk)
        except FarmDocument.DoesNotExist:
            return None

    @sync_to_async
    def list(self) -> List[FarmDocument]:
        return list(FarmDocument.objects.all().select_related('farm'))

    @sync_to_async
    def create(self, data: FarmDocumentCreateUpdateSchema) -> FarmDocument:
        # farm instance get by farm_id for FK
        from apps.farm.models import Farm
        farm = Farm.objects.get(id=data.farm_id)
        document = FarmDocument(
            farm=farm,
            document_type=data.document_type,
            title=data.title,
            issue_date=data.issue_date,
            expiry_date=data.expiry_date,
            description=data.description,
        )
        document.save()
        return document

    @sync_to_async
    def update(self, document: FarmDocument, data: FarmDocumentCreateUpdateSchema) -> FarmDocument:
        document.document_type = data.document_type
        document.title = data.title
        document.issue_date = data.issue_date
        document.expiry_date = data.expiry_date
        document.description = data.description
        document.save()
        return document

    @sync_to_async
    def delete(self, document: FarmDocument) -> None:
        document.delete()
