from fastapi import APIRouter

from src.apps.user.schema import UserCreateSchema, UserRegistrySchema, LoginSchema
from src.apps.user.use_cases.login_use_case import UserLoginUseCase
from src.apps.user.use_cases.register_use_case import UserRegistryUseCase

user_router = APIRouter(prefix='/user')


@user_router.post('/register')
async def user_register(params: UserRegistrySchema, user_registry_use_case: UserRegistryUseCase):
    """
    Регистрация пользователя.
    :param params:
    :param user_registry_use_case: UserRegistryUseCase
    :return: UserReadSchema
    """

    return await user_registry_use_case(params)


@user_router.post('/login')
async def login(params: LoginSchema, user_login_use_case: UserLoginUseCase):
    """
    Авторизация пользователя.
    :param params: LoginSchema
    :param user_login_use_case: UserLoginUseCase
    :return: UserReadSchema
    """

    return await user_login_use_case(params)
