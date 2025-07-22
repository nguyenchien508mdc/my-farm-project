# apps/farm/mappers/farm_mapper.py
from typing import Optional
from apps.farm.models import Farm
from apps.farm.schemas.farm import FarmOutSchema, FarmCreateUpdateSchema


def farm_to_schema(farm: Farm) -> FarmOutSchema:
    return FarmOutSchema(
        id=farm.id,
        name=farm.name,
        slug=farm.slug,
        location=farm.location,
        area=farm.area,
        farm_type=farm.farm_type,
        farm_type_display=farm.get_farm_type_display() if hasattr(farm, 'get_farm_type_display') else "",
        description=farm.description,
        is_active=farm.is_active,
        established_date=farm.established_date,
        logo=farm.logo.url if (farm.logo and hasattr(farm.logo, 'url')) else None,
        members_count=farm.farmmembership_set.count() if hasattr(farm, 'farmmembership_set') else 0,
        active_members_count=farm.farmmembership_set.filter(is_active=True).count() if hasattr(farm, 'farmmembership_set') else 0,
        created_at=farm.created_at,
        updated_at=farm.updated_at,
    )


def create_farm_from_schema(schema: FarmCreateUpdateSchema) -> Farm:
    farm = Farm(
        name=schema.name,
        location=schema.location,
        area=schema.area,
        farm_type=schema.farm_type,
        description=schema.description,
        is_active=schema.is_active,
        established_date=schema.established_date,
    )

    if schema.logo:
        farm.logo = schema.logo  # logo phải là file, không phải string URL hay base64

    return farm



def update_farm_from_schema(farm: Farm, schema: FarmCreateUpdateSchema) -> Farm:
    farm.name = schema.name
    farm.location = schema.location
    farm.area = schema.area
    farm.farm_type = schema.farm_type
    farm.description = schema.description
    farm.is_active = schema.is_active
    farm.established_date = schema.established_date
    if schema.logo:
        farm.logo = schema.logo
    return farm
