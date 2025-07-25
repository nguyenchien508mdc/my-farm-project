# apps/farm/schemas/document_schema.py
from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, validator, constr, ConfigDict
from apps.farm.schemas.farm_schema import FarmOutSchema 

class FarmDocumentSchema(BaseModel):
    document_type: constr(min_length=1, max_length=50)
    title: constr(min_length=1, max_length=255)
    issue_date: date
    expiry_date: Optional[date] = None
    description: Optional[str] = None
    file_url: Optional[str] = None  

    @validator('expiry_date')
    def expiry_must_be_after_issue(cls, v, values):
        issue_date = values.get('issue_date')
        if v and issue_date and v < issue_date:
            raise ValueError('Ngày hết hạn phải sau ngày phát hành')
        return v

class FarmDocumentCreateUpdateSchema(BaseModel):
    farm_id: int
    document_type: constr(min_length=1, max_length=50)
    title: constr(min_length=1, max_length=255) 
    issue_date: date
    expiry_date: Optional[date] = None
    description: Optional[str] = None

    @validator('expiry_date')
    def expiry_must_be_after_issue(cls, v, values):
        issue_date = values.get('issue_date')
        if v and issue_date and v < issue_date:
            raise ValueError('Ngày hết hạn phải sau ngày phát hành')
        return v

class FarmDocumentOutSchema(FarmDocumentSchema):
    id: int
    farm: Optional[FarmOutSchema] = None
    document_type_display: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

