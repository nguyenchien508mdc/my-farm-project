# apps/farm/repositories/document/base.py
from abc import ABC, abstractmethod
from typing import List, Optional
from apps.farm.schemas.document_schema import FarmDocumentCreateUpdateSchema
from apps.farm.models import FarmDocument

class AbstractFarmDocumentRepository(ABC):
    @abstractmethod
    async def get(self, pk: int) -> Optional[FarmDocument]:
        pass

    @abstractmethod
    async def list(self) -> List[FarmDocument]:
        pass

    @abstractmethod
    async def create(self, data: FarmDocumentCreateUpdateSchema) -> FarmDocument:
        pass

    @abstractmethod
    async def update(self, doc: FarmDocument, data: FarmDocumentCreateUpdateSchema) -> FarmDocument:
        pass

    @abstractmethod
    async def delete(self, doc: FarmDocument) -> None:
        pass

