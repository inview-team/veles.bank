from uuid import UUID

from pydantic import BaseModel, Field


class CompanyBaseSchema(BaseModel):
    id: UUID
    name: str
    email: str


class CompanyReadSchema(CompanyBaseSchema):
    ...


class CompanyCreateSchema(CompanyBaseSchema):
    balance: float = Field(default=0.0)


class CompanyUpdateSchema(BaseModel):
    balance: float
