from fastapi import APIRouter, Depends

from src.apps.auth.depends import get_current_user
from src.apps.company.schema import CompanyReadSchema
from src.apps.company.use_cases.company_list_use_case import CompanyListUseCase

company_router = APIRouter(prefix='/company')


@company_router.get('/', response_model=list[CompanyReadSchema], dependencies=[Depends(get_current_user)])
async def get_all_companies(company_use_case: CompanyListUseCase):
    return await company_use_case()
