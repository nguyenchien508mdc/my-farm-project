# apps/farm/repositories/farm/base.py

from abc import ABC, abstractmethod
from typing import List, Optional
from apps.farm.schemas.farm_schema import FarmCreateUpdateSchema
from apps.farm.models import Farm

class AbstractFarmRepository(ABC):
    @abstractmethod
    async def get(self, pk: int) -> Optional[Farm]:
        pass

    @abstractmethod
    async def list(self) -> List[Farm]:
        pass

    @abstractmethod
    async def create(self, data: FarmCreateUpdateSchema) -> Farm:
        pass

    @abstractmethod
    async def update(self, farm: Farm, data: FarmCreateUpdateSchema) -> Farm:
        pass

    @abstractmethod
    async def delete(self, farm: Farm) -> None:
        pass

