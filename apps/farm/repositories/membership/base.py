from abc import ABC, abstractmethod
from typing import List, Optional

from apps.farm.models import FarmMembership
from apps.farm.schemas.membership_schema import FarmMembershipCreateUpdateSchema


class AbstractFarmMembershipRepository(ABC):
    @abstractmethod
    async def get(self, pk: int) -> Optional[FarmMembership]: 
        pass

    @abstractmethod
    async def list(self) -> List[FarmMembership]: 
        pass

    @abstractmethod
    async def create(self, data: FarmMembershipCreateUpdateSchema) -> FarmMembership: 
        pass

    @abstractmethod
    async def update(self, instance: FarmMembership, data: FarmMembershipCreateUpdateSchema) -> FarmMembership: 
        pass

    @abstractmethod
    async def delete(self, instance: FarmMembership) -> None: 
        pass

    @abstractmethod
    async def get_by_user_farm(self, user_id: int, farm_id: int) -> Optional[FarmMembership]:
        pass
