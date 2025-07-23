# apps/farm/mappers/document_mapper.py
import os
from typing import Optional

from apps.farm.models import FarmDocument, Farm
from apps.farm.schemas.document_schema import FarmDocumentOutSchema, FarmDocumentCreateUpdateSchema
from apps.farm.schemas.farm_schema import FarmOutSchema


def minimal_farm_schema(farm: Optional[Farm]) -> Optional[FarmOutSchema]:
    if not farm:
        return None

    return FarmOutSchema(
        id=farm.id,
        name=farm.name,
        slug=farm.slug,
        location=farm.location or None,
        area=farm.area or 0.0,
        farm_type=farm.farm_type or "",
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


def document_to_schema(doc: FarmDocument) -> FarmDocumentOutSchema:
    file_url = None
    try:
        if doc.file and hasattr(doc.file, 'url') and os.path.exists(doc.file.path):
            file_url = doc.file.url
    except Exception:
        file_url = None

    return FarmDocumentOutSchema(
        id=doc.id,
        farm=minimal_farm_schema(doc.farm),
        document_type=doc.document_type,
        document_type_display=doc.get_document_type_display(),
        title=doc.title,
        file_url=file_url,
        issue_date=doc.issue_date,
        expiry_date=doc.expiry_date,
        description=doc.description,
        created_at=doc.created_at,
        updated_at=doc.updated_at,
    )


def create_document_from_schema(schema: FarmDocumentCreateUpdateSchema, farm: Optional[Farm] = None) -> FarmDocument:
    doc = FarmDocument()

    # Gán farm nếu truyền vào hoặc từ schema
    if farm:
        doc.farm = farm
    else:
        # schema.farm là int (id), lấy farm object
        doc.farm = Farm.objects.get(id=schema.farm_id)

    doc.document_type = schema.document_type
    doc.title = schema.title
    doc.issue_date = schema.issue_date
    doc.expiry_date = schema.expiry_date
    doc.description = schema.description
    # file xử lý riêng (file upload)
    return doc


def update_document_from_schema(doc: FarmDocument, schema: FarmDocumentCreateUpdateSchema) -> FarmDocument:
    doc.document_type = schema.document_type
    doc.title = schema.title
    doc.issue_date = schema.issue_date
    doc.expiry_date = schema.expiry_date
    doc.description = schema.description
    return doc
