from typing import Protocol, Annotated

from fastapi import Depends
from fastapi import Response
from starlette.responses import JSONResponse

from src.apps.auth.service import AuthServiceProtocol, AuthService
from src.apps.user.schema import UserCreateSchema, UserReadSchema, UserRegistrySchema
from src.apps.user.service import UserServiceProtocol, UserService


class UserRegistryUseCaseProtocol(Protocol):
    """
    Базовый интерфейс юз-кейса регистрации пользователя
    """

    async def __call__(self) -> UserReadSchema:
        ...

    async def make_response(self, status, data) -> Response:
        ...


class UserRegistryUseCaseImpl:
    """
    Реализация юз-кейса регистрации пользователя
    """

    def __init__(self, user_service: UserServiceProtocol, auth_service: AuthServiceProtocol):
        self.user_service = user_service
        self.auth_service = auth_service

    async def __call__(self, params: UserRegistrySchema) -> Response:
        user = await self.user_service.registry_user(params=params)
        token_dto = await self.auth_service.create(user)
        return await self.make_response(
            status=201, content={"id": str(user.id), **user.model_dump(exclude={"id"}), "access_token": token_dto.access},
        )

    async def make_response(self, status, content) -> Response:
        refresh_token = content.pop("refresh")
        response = JSONResponse(content=content, status_code=status)
        response.set_cookie(key="refresh", value=refresh_token, httponly=True)

        return response


async def get_user_registry_use_case(user_service: UserService, auth_service: AuthService) -> UserRegistryUseCaseImpl:
    return UserRegistryUseCaseImpl(user_service, auth_service)


UserRegistryUseCase = Annotated[UserRegistryUseCaseProtocol, Depends(get_user_registry_use_case)]
