from typing import Protocol, Annotated

from fastapi import Depends, HTTPException

from src.apps.user.repository import UserRepositoryProtocol, UserRepository
from src.apps.user.schema import UserCreateSchema, UserReadSchema, LoginSchema, UserRegistrySchema
from src.core.repository import BaseRepositoryProtocol


class UserServiceProtocol(Protocol):
    """
    Базовый интерфейс сервиса пользователя.
    """

    async def registry_user(self, params: UserRegistrySchema) -> UserReadSchema:
        ...

    async def login(self, params: LoginSchema) -> UserReadSchema:
        ...


class UserServiceImpl(UserServiceProtocol):
    """
    Реализация сервиса пользователя.
    """

    def __init__(self, user_repository: UserRepositoryProtocol):
        self.user_repository = user_repository

    async def registry_user(self, params: UserRegistrySchema) -> UserReadSchema:
        """
        Метод сервиса регистрация пользователя.
        :param params: UserCreateSchema
        :return: UserReadSchema
        """

        user = await self.user_repository.get_user_by_email(params.email)
        if user:
            raise HTTPException(status_code=400, detail='User already exists.')
        if params.password != params.password2:
            raise HTTPException(status_code=400, detail="Passwords don't match.")
        user_dto = UserCreateSchema(**params.model_dump(exclude={'password2'}))
        return await self.user_repository.create(user_dto)

    async def login(self, params: LoginSchema) -> UserReadSchema:
        """
        Метод сервиса авторизации пользователя.
        :param params: LoginSchema
        :return: UserReadSchema
        """

        user = await self.user_repository.get_user_by_email(params.email)
        if not user:
            raise HTTPException(status_code=400, detail='User not found.')
        if user.password != params.password:
            raise HTTPException(status_code=400, detail='Wrong password.')

        return UserReadSchema(**user.model_dump(exclude={'password'}))


async def get_user_service(user_repository: UserRepository) -> UserServiceProtocol:
    return UserServiceImpl(user_repository)


UserService = Annotated[UserServiceImpl, Depends(get_user_service)]
