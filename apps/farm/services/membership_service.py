from typing import List, Optional

from apps.farm.models import FarmMembership
from apps.farm.schemas.membership_schema import FarmMembershipCreateUpdateSchema
from apps.farm.repositories.membership.factory import get_membership_repository


class FarmMembershipService:
    def __init__(self):
        self.repo = get_membership_repository()

    async def get_membership(self, pk: int) -> Optional[FarmMembership]:
        return await self.repo.get(pk)

    async def list_memberships(self) -> List[FarmMembership]:
        return await self.repo.list()

    async def create_membership(self, data: FarmMembershipCreateUpdateSchema) -> FarmMembership:
        return await self.repo.create(data)

    async def update_membership(self, pk: int, data: FarmMembershipCreateUpdateSchema) -> FarmMembership:
        instance = await self.repo.get(pk)
        if not instance:
            raise ValueError("Membership not found")
        return await self.repo.update(instance, data)

    async def delete_membership(self, pk: int) -> None:
        instance = await self.repo.get(pk)
        if not instance:
            raise ValueError("Membership not found")
        await self.repo.delete(instance)
