from typing import Protocol, Annotated

from fastapi import Depends, Response
from starlette.responses import JSONResponse

from src.apps.auth.schema import LoginResponseSchema
from src.apps.auth.service import AuthServiceProtocol, AuthService
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

    def __init__(self, user_service: UserServiceProtocol, auth_service: AuthServiceProtocol):
        self.user_service = user_service
        self.auth_service = auth_service

    async def __call__(self, params: LoginSchema):
        user = await self.user_service.login(params)
        token_dto = await self.auth_service.create(user)
        return LoginResponseSchema(**user.model_dump(exclude={'password'}), **token_dto.model_dump())


async def get_user_login_use_case(user_service: UserService, auth_service: AuthService) -> UserLoginUseCaseImpl:
    return UserLoginUseCaseImpl(user_service, auth_service)


UserLoginUseCase = Annotated[UserLoginUseCaseImpl, Depends(get_user_login_use_case)]
