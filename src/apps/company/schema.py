from uuid import UUID

from pydantic import BaseModel, Field


class CompanyBaseSchema(BaseModel):
    id: UUID
    name: str
    email: str


class CompanyReadSchema(CompanyBaseSchema):
    ...


class CompanyCreateSchema(CompanyBaseSchema):
    ...


class CompanyUpdateSchema(BaseModel):
    ...

