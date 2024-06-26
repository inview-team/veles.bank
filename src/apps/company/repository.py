from typing import Annotated

from fastapi import Depends

from src.apps.company.model import Company
from src.apps.company.schema import CompanyReadSchema, CompanyCreateSchema, CompanyUpdateSchema
from src.core.db import Session
from src.core.repository import BaseRepositoryProtocol, BaseRepositoryImpl
import sqlalchemy as sa


class CompanyRepositoryProtocol(
    BaseRepositoryProtocol[Company, CompanyReadSchema, CompanyCreateSchema, CompanyUpdateSchema]
):
    async def get_all_companies(self) -> list[CompanyReadSchema]:
        ...

    async def get_by_name(self, name: str) -> CompanyReadSchema | None:
        ...


class CompanyRepositoryImpl(
    BaseRepositoryImpl[Company, CompanyReadSchema, CompanyCreateSchema, CompanyUpdateSchema], CompanyRepositoryProtocol
):
    async def get_all_companies(self) -> list[CompanyReadSchema]:
        async with self.session as s:
            statement = sa.select(self.model_type)
            model = (await s.execute(statement)).scalars().all()
            return [self.read_schema_type.model_validate(m, from_attributes=True) for m in model]

    async def get_by_name(self, name: str) -> CompanyReadSchema | None:
        async with self.session as s:
            statement = sa.select(self.model_type).where(self.model_type.name == name)
            model = (await s.execute(statement)).scalar_one_or_none()
            if model is None:
                return None
            return self.read_schema_type.model_validate(model, from_attributes=True)


async def get_company_repository(session: Session) -> CompanyRepositoryProtocol:
    return CompanyRepositoryImpl(session)


CompanyRepository = Annotated[CompanyRepositoryProtocol, Depends(get_company_repository)]
