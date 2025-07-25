# apps/farm/services/document_service.py

from typing import List, Optional
from apps.farm.repositories.document.factory import get_document_repository
from apps.farm.schemas.document_schema import FarmDocumentCreateUpdateSchema
from apps.farm.models import FarmDocument

class DocumentService:
    def __init__(self):
        self.repo = get_document_repository()

    async def get_document(self, pk: int) -> Optional[FarmDocument]:
        return await self.repo.get(pk)

    async def list_documents(self) -> List[FarmDocument]:
        return await self.repo.list()

    async def create_document(self, data: FarmDocumentCreateUpdateSchema) -> FarmDocument:
        return await self.repo.create(data)

    async def update_document(self, pk: int, data: FarmDocumentCreateUpdateSchema) -> FarmDocument:
        document = await self.repo.get(pk)
        if not document:
            raise ValueError("Document not found")
        return await self.repo.update(document, data)

    async def delete_document(self, pk: int) -> None:
        document = await self.repo.get(pk)
        if not document:
            raise ValueError("Document not found")
        await self.repo.delete(document)
