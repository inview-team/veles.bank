from typing import Protocol, Annotated

from fastapi import Depends

from src.apps.auth.depends import CurrentUserFromRefresh
from src.apps.auth.schema import AuthSmallReadSchema
from src.apps.auth.service import AuthServiceProtocol, AuthService
from src.apps.user.schema import UserReadSchema


class AuthRefreshUseCaseProtocol(Protocol):

    async def __call__(self) -> AuthSmallReadSchema:
        ...


class AuthRefreshUseCaseImpl:

    def __init__(
        self,
        auth_service: AuthServiceProtocol,
        user: UserReadSchema,
    ):
        self.auth_service = auth_service
        self.user = user

    async def __call__(self) -> AuthSmallReadSchema:
        return await self.auth_service.refresh_tokens(self.user)


async def get_auth_refresh_use_case(
    auth_service: AuthService,
    user: CurrentUserFromRefresh
) -> AuthRefreshUseCaseImpl:
    return AuthRefreshUseCaseImpl(auth_service, user)


AuthRefreshUseCase = Annotated[AuthRefreshUseCaseProtocol, Depends(get_auth_refresh_use_case)]
