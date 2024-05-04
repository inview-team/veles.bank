from typing import Annotated

from fastapi import Depends
from pydantic import (
    BaseModel,
)

from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = (
    'get_settings',
    'Settings',
    'settings',
    'SettingsService',
)


class Db(BaseModel):
    """
    Настройки для подключения к базе данных.
    """

    host: str
    port: int
    user: str
    password: str
    name: str

    provider: str = 'postgresql+psycopg_async'

    @property
    def dsn(self) -> str:
        return f'{self.provider}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'


class Settings(BaseSettings):
    """
    Настройки модели.
    """

    debug: bool

    db: Db

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
        case_sensitive=False,
        extra='ignore',
    )


def get_settings() -> Settings:
    return Settings()  # type: ignore


settings = get_settings()

SettingsService = Annotated[Settings, Depends(get_settings)]
