from typing import Protocol, Annotated

from fastapi import Depends

from src.apps.company.repository import CompanyRepositoryProtocol, CompanyRepository
from src.apps.company.schema import CompanyReadSchema


class CompanyServiceProtocol(Protocol):
    async def get_company_list(self) -> list[CompanyReadSchema]:
        ...


class CompanyServiceImpl(CompanyServiceProtocol):
    def __init__(self, company_repository: CompanyRepositoryProtocol):
        self.company_repository = company_repository

    async def get_company_list(self) -> list[CompanyReadSchema]:
        return await self.company_repository.get_all_companies()


async def get_company_service(company_repository: CompanyRepository) -> CompanyServiceProtocol:
    return CompanyServiceImpl(company_repository)


CompanyService = Annotated[CompanyServiceProtocol, Depends(get_company_service)]
