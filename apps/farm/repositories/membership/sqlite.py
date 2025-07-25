from typing import List, Optional
from asgiref.sync import sync_to_async

from apps.farm.models import FarmMembership, Farm
from apps.farm.schemas.membership_schema import FarmMembershipCreateUpdateSchema
from apps.farm.repositories.membership.base import AbstractFarmMembershipRepository


class SqliteFarmMembershipRepository(AbstractFarmMembershipRepository):

    @sync_to_async
    def get(self, pk: int) -> Optional[FarmMembership]:
        try:
            return FarmMembership.objects.select_related('user', 'farm').get(pk=pk)
        except FarmMembership.DoesNotExist:
            return None

    @sync_to_async
    def list(self) -> List[FarmMembership]:
        return list(FarmMembership.objects.select_related('user', 'farm').all())

    @sync_to_async
    def create(self, data: FarmMembershipCreateUpdateSchema) -> FarmMembership:
        from apps.core.models import User
        farm = Farm.objects.get(id=data.farm_id)
        user = User.objects.get(id=data.user_id)
        membership = FarmMembership(
            farm=farm,
            user=user,
            role=data.role,
            is_active=data.is_active,
            can_approve=data.can_approve,
        )
        membership.save()
        return membership

    @sync_to_async
    def update(self, instance: FarmMembership, data: FarmMembershipCreateUpdateSchema) -> FarmMembership:
        instance.role = data.role
        instance.is_active = data.is_active
        instance.can_approve = data.can_approve
        instance.save()
        return instance

    @sync_to_async
    def delete(self, instance: FarmMembership) -> None:
        instance.delete()

    async def get_by_user_farm(self, user_id: int, farm_id: int) -> Optional[FarmMembership]:
        @sync_to_async
        def _get():
            try:
                return FarmMembership.objects.get(user_id=user_id, farm_id=farm_id, is_active=True)
            except FarmMembership.DoesNotExist:
                return None
        return await _get()