from fastapi import APIRouter

from src.apps.auth.use_cases.auth_use_case import AuthRefreshUseCase

auth_router = APIRouter(prefix='')


@auth_router.post('/refresh')
async def refresh(auth_use_case: AuthRefreshUseCase):
    """
    Обновление токена
    :param auth_use_case:
    :return:
    """

    return await auth_use_case()
