import logging
import uuid
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError

from src.apps.auth.repository import AuthRepository
from src.apps.auth.schema import RefreshRequestSchema
from src.apps.user.repository import UserRepositoryProtocol, get_user_repository, UserRepository
from src.apps.user.schema import UserReadSchema
from src.settings import settings


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    user_repository: UserRepository,
) -> UserReadSchema:
    try:
        token = jwt.decode(credentials.credentials, key=settings.secret, algorithms=[settings.algorithm])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return await user_repository.get(token['sub'])


CurrentUser = Annotated[UserReadSchema, Depends(get_current_user)]


async def get_current_user_from_refresh(
    user_repository: UserRepository,
    auth_repository: AuthRepository,
    params: RefreshRequestSchema,
) -> UserReadSchema:
    token = await auth_repository.get_by_token(value=params.refresh, type="refresh")
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    try:
        token = jwt.decode(params.refresh, key=settings.secret, algorithms=[settings.algorithm])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return await user_repository.get(token['sub'])

CurrentUserFromRefresh = Annotated[UserReadSchema, Depends(get_current_user_from_refresh)]
