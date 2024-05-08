from typing import Protocol, Annotated
from fastapi import Depends

from src.apps.company.schema import CompanyReadSchema
from src.apps.company.service import CompanyServiceProtocol, CompanyService


class CompanyListUseCaseProtocol(Protocol):
    async def __call__(self) -> list[CompanyReadSchema]:
        ...


class CompanyListUseCaseImpl:
    def __init__(self, company_service: CompanyServiceProtocol) -> None:
        self.company_service = company_service

    async def __call__(self) -> list[CompanyReadSchema]:
        return await self.company_service.get_company_list()


async def get_company_list_use_case(company_service: CompanyService) -> CompanyListUseCaseImpl:
    return CompanyListUseCaseImpl(company_service)


CompanyListUseCase = Annotated[CompanyListUseCaseProtocol, Depends(get_company_list_use_case)]
