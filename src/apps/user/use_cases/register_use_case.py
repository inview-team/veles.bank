from typing import Protocol, Annotated

from fastapi import Depends

from src.apps.user.schema import UserCreateSchema, UserReadSchema, UserRegistrySchema
from src.apps.user.service import UserServiceProtocol, UserService


class UserRegistryUseCaseProtocol(Protocol):
    """
    Базовый интерфейс юз-кейса регистрации пользователя
    """

    async def __call__(self) -> UserReadSchema:
        ...


class UserRegistryUseCaseImpl:
    """
    Реализация юз-кейса регистрации пользователя
    """

    def __init__(self, user_service: UserServiceProtocol):
        self.user_service = user_service

    async def __call__(self, params: UserRegistrySchema) -> UserReadSchema:
        return await self.user_service.registry_user(params=params)


async def get_user_registry_use_case(user_service: UserService) -> UserRegistryUseCaseImpl:
    return UserRegistryUseCaseImpl(user_service)

UserRegistryUseCase = Annotated[UserRegistryUseCaseProtocol, Depends(get_user_registry_use_case)]
