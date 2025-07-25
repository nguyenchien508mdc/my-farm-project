# apps/farm/services/farm_service.py

from typing import List
from pydantic import ValidationError

from apps.farm.models import Farm
from apps.farm.schemas.farm_schema import FarmCreateUpdateSchema
from apps.farm.repositories.farm.factory import get_farm_repository
from apps.farm.mappers.farm_mapper import farm_to_schema


farm_repo = get_farm_repository() 


class FarmService:

    async def get_farm(self, farm_id: int) -> Farm:
        farm = await farm_repo.get(farm_id)
        if not farm:
            raise ValueError("Nông trại không tồn tại")
        return farm

    async def list_farms(self) -> List[Farm]:
        farms = await farm_repo.list()
        return farms

    async def create_farm(self, data: dict) -> Farm:
        try:
            schema = FarmCreateUpdateSchema(**data)
        except ValidationError as e:
            raise ValueError(f"Validation failed: {e}")

        farm = await farm_repo.create(schema)
        return farm

    async def update_farm(self, farm_id: int, data: dict) -> Farm:
        farm = await self.get_farm(farm_id)

        try:
            schema = FarmCreateUpdateSchema(**data)
        except ValidationError as e:
            raise ValueError(f"Validation failed: {e}")

        farm = await farm_repo.update(farm, schema)
        return farm

    async def delete_farm(self, farm_id: int) -> None:
        farm = await self.get_farm(farm_id)
        await farm_repo.delete(farm)
