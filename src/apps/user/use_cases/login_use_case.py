from typing import Protocol, Annotated

from fastapi import Depends

from src.apps.user.repository import UserRepositoryProtocol
from src.apps.user.schema import LoginSchema
from src.apps.user.service import UserServiceProtocol, UserService


class UserLoginUseCaseProtocol(Protocol):
    async def login(self) -> str:
        ...


class UserLoginUseCaseImpl:
    """
    Юз-кейс авторизация пользователя.
    """

    def __init__(self, user_service: UserServiceProtocol):
        self.user_service = user_service

    async def __call__(self, params: LoginSchema):
        return await self.user_service.login(params)


async def get_user_login_use_case(user_service: UserService) -> UserLoginUseCaseImpl:
    return UserLoginUseCaseImpl(user_service)


UserLoginUseCase = Annotated[UserLoginUseCaseImpl, Depends(get_user_login_use_case)]
