from typing import Annotated

from fastapi import APIRouter, Depends, Body

from src.apps.auth.depends import CurrentUser
from src.apps.user.schema import UserCreateSchema, UserRegistrySchema, LoginSchema, UserResponseSchema, UserMeSchema
from src.apps.user.use_cases.login_use_case import UserLoginUseCase
from src.apps.user.use_cases.me_use_case import UserMeUseCase
from src.apps.user.use_cases.register_use_case import UserRegistryUseCase

user_router = APIRouter(prefix='')


@user_router.post('/register', response_model=UserResponseSchema)
async def user_register(
        params: Annotated[UserRegistrySchema,
        Body(example={
            "first_name": "Mike",
            "last_name": "Bobov",
            "email": "mtstruetech@example.com",
            "phone_number": "89234567890",
            "password": "12345678",
            "password2": "12345678"}, )
        ],
        user_registry_use_case: UserRegistryUseCase
):
    """
    Регистрация пользователя.
    :param params:
    :param user_registry_use_case: UserRegistryUseCase
    :return: UserReadSchema
    """

    return await user_registry_use_case(params)


@user_router.post('/login', response_model=UserResponseSchema)
async def login(
        params: Annotated[LoginSchema,
        Body(example={"email": "mtstruetech@example.com", "password": "12345678"})],
        user_login_use_case: UserLoginUseCase,
):
    """
    Авторизация пользователя.
    :param params: LoginSchema
    :param user_login_use_case: UserLoginUseCase
    :return: UserReadSchema
    """

    return await user_login_use_case(params)


@user_router.get('/me', response_model=UserMeSchema)
async def me(user_me: UserMeUseCase):
    return await user_me()
