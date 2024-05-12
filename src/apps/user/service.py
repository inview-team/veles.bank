from typing import Protocol, Annotated

import sqlalchemy
from fastapi import Depends, HTTPException

from src.apps.company.utils import rebuild_phone_number
from src.apps.user.repository import UserRepositoryProtocol, UserRepository
from src.apps.user.schema import UserCreateSchema, UserReadSchema, LoginSchema, UserRegistrySchema, UserMeSchema
from src.core.repository import BaseRepositoryProtocol
from src.apps.user.utils.string import get_password_hash, verify_password


class UserServiceProtocol(Protocol):
    """
    Базовый интерфейс сервиса пользователя.
    """

    async def registry_user(self, params: UserRegistrySchema) -> UserReadSchema:
        ...

    async def login(self, params: LoginSchema) -> UserReadSchema:
        ...

    async def me(self, user: UserReadSchema) -> UserMeSchema:
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
        user_dto = UserCreateSchema(
            password=get_password_hash(params.password),
            phone_number=(await rebuild_phone_number(params.phone_number)),
            **params.model_dump(exclude={'password2', 'password', 'phone_number'})
        )
        try:
            user = await self.user_repository.create(user_dto)
        except sqlalchemy.exc.IntegrityError as exc:
            raise HTTPException(status_code=400, detail="User with these phone_number already exist.") from exc
        return user

    async def login(self, params: LoginSchema) -> UserReadSchema:
        """
        Метод сервиса авторизации пользователя.
        :param params: LoginSchema
        :return: UserReadSchema
        """

        user = await self.user_repository.get_user_by_email(params.email)
        if not user:
            raise HTTPException(status_code=400, detail='User not found.')
        if not verify_password(params.password, user.password):
            raise HTTPException(status_code=400, detail='Incorrect login or password')

        return UserReadSchema(**user.model_dump(exclude={'password'}))

    async def me(self, user: UserReadSchema) -> UserMeSchema:
        return UserMeSchema(**user.model_dump())


async def get_user_service(user_repository: UserRepository) -> UserServiceProtocol:
    return UserServiceImpl(user_repository)


UserService = Annotated[UserServiceImpl, Depends(get_user_service)]
