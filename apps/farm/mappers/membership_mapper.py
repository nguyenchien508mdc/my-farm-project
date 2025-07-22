# apps/farm/mappers/membership_mapper.py
from apps.farm.models import FarmMembership
from apps.farm.schemas.membership import FarmMembershipOutSchema, FarmMembershipCreateUpdateSchema
from apps.farm.mappers.farm_mapper import farm_to_schema
from apps.core.mappers.user_mapper import user_to_schema


def membership_to_schema(m: FarmMembership) -> FarmMembershipOutSchema:
    return FarmMembershipOutSchema(
        id=m.id,
        farm=farm_to_schema(m.farm),
        user=user_to_schema(m.user),
        role=m.role,
        role_display=m.get_role_display(),
        joined_date=m.joined_date,
        is_active=m.is_active,
        can_approve=m.can_approve,
        created_at=m.created_at,
        updated_at=m.updated_at,
    )


def create_membership_from_schema(schema: FarmMembershipCreateUpdateSchema) -> FarmMembership:
    """
    Dùng để tạo mới FarmMembership.
    Chú ý: schema.farm và schema.user là int (id), nên cần lấy instance từ DB.
    """
    from apps.farm.models import Farm
    from apps.core.models import User

    farm_instance = Farm.objects.get(id=schema.farm_id)
    user_instance = User.objects.get(id=schema.user_id)

    return FarmMembership(
        farm=farm_instance,
        user=user_instance,
        role=schema.role,
        is_active=schema.is_active,
        can_approve=schema.can_approve
    )


def update_membership_from_schema(instance: FarmMembership, schema: FarmMembershipCreateUpdateSchema) -> FarmMembership:
    """
    Dùng để cập nhật FarmMembership hiện có. Không đổi user & farm.
    """
    instance.role = schema.role
    instance.is_active = schema.is_active
    instance.can_approve = schema.can_approve
    return instance
