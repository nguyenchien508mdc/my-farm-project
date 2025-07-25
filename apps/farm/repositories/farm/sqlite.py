# apps/farm/repositories/farm/sqlite.py

from typing import List, Optional
from apps.farm.models import Farm
from apps.farm.schemas.farm_schema import FarmCreateUpdateSchema
from apps.farm.repositories.farm.base import AbstractFarmRepository
from apps.farm.mappers.farm_mapper import create_farm_from_schema, update_farm_from_schema

class SqliteFarmRepository(AbstractFarmRepository):

    async def get(self, pk: int) -> Optional[Farm]:
        try:
            farm = await Farm.objects.aget(pk=pk)
            return farm
        except Farm.DoesNotExist:
            return None

    async def list(self) -> List[Farm]:
        farms = []
        async for farm in Farm.objects.all():
            farms.append(farm)
        return farms

    async def create(self, data: FarmCreateUpdateSchema) -> Farm:
        farm = create_farm_from_schema(data)
        await farm.asave()  # async save
        return farm

    async def update(self, farm: Farm, data: FarmCreateUpdateSchema) -> Farm:
        farm = update_farm_from_schema(farm, data)
        await farm.asave()  # async save
        return farm

    async def delete(self, farm: Farm) -> None:
        await farm.adelete()  # async delete

