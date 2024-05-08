from typing import Protocol, Annotated

from fastapi import Depends
from jose import jwt
from datetime import datetime, timedelta

from src.apps.auth.depends import CurrentUserFromRefresh
from src.apps.auth.repository import AuthRepositoryProtocol, AuthRepository
from src.apps.auth.schema import AuthCreateSchema, AuthReadSchema, AuthSmallReadSchema, AuthGenerateSchema
from src.apps.user.schema import UserReadSchema
from src.settings import Settings, SettingsService


class AuthServiceProtocol(Protocol):
    ...

    async def create_token(self, user: UserReadSchema, token_ttl: int, token_type: str) -> str:
        ...

    async def create(self, user: UserReadSchema) -> AuthSmallReadSchema:
        ...

    async def refresh_tokens(self, user: UserReadSchema) -> AuthSmallReadSchema:
        ...


class AuthServiceImpl(AuthServiceProtocol):

    def __init__(self, auth_repository: AuthRepositoryProtocol, settings: Settings):
        self.auth_repository = auth_repository
        self.settings = settings

    async def create_token(self, user: UserReadSchema, token_ttl: int, token_type: str) -> str:
        """
        Метод генерации токена
        :param user: UserReadSchema
        :param token_ttl: int
        :param token_type: str
        :return: str
        """

        token = await self.auth_repository.get_by_user_id(user.id, token_type)
        if token:
            return token.token
        exp = datetime.utcnow() + timedelta(minutes=token_ttl)
        claim = AuthGenerateSchema(
            sub=str(user.id),
            email=user.email,
            exp=exp
        )
        token = jwt.encode(claim.model_dump(), key=self.settings.secret, algorithm=self.settings.algorithm)
        return token

    async def create(self, user: UserReadSchema) -> AuthSmallReadSchema:
        """
        Метод создания пары токенов
        :param user: UserReadSchema
        :return: AuthSmallReadSchema
        """

        access = await self.create_token(user, self.settings.access_exp, "access")
        refresh = await self.create_token(user, self.settings.refresh_exp, "refresh")

        token_dto = AuthCreateSchema(token=access, type="access", user_id=user.id)
        await self.auth_repository.create(token_dto)

        token_dto = AuthCreateSchema(token=refresh, type="refresh", user_id=user.id)
        await self.auth_repository.create(token_dto)

        return AuthSmallReadSchema(access=access, refresh=refresh)

    async def refresh_tokens(self, user: UserReadSchema) -> AuthSmallReadSchema:
        """
        Метод обновления токенов
        :param user:
        :return:
        """

        await self.auth_repository.delete_by_type_user_id(user_id=user.id, token_type="access")
        await self.auth_repository.delete_by_type_user_id(user_id=user.id, token_type="refresh")

        return await self.create(user)


async def get_auth_service(auth_repository: AuthRepository, settings: SettingsService) -> AuthServiceProtocol:
    return AuthServiceImpl(auth_repository, settings)


AuthService = Annotated[AuthServiceImpl, Depends(get_auth_service)]
