from typing import Annotated, AsyncGenerator
from uuid import UUID, uuid4

from fastapi import Depends
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

__all__ = (
    'Base',
    'Session',
    'AsyncSession',
    'get_async_session',
    'BASE_ID',
)

from src.settings import settings

asyncio_engine = create_async_engine(settings.db.dsn, echo=True)
AsyncSessionFactory = async_sessionmaker(
    asyncio_engine,
    autocommit=False,
    expire_on_commit=False,
    future=True,
    autoflush=False,)

BASE_ID = UUID


class Base(AsyncAttrs, DeclarativeBase):
    metadata = MetaData()

    id: Mapped[BASE_ID] = mapped_column(primary_key=True, default=uuid4)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        yield session


Session = Annotated[AsyncSession, Depends(get_async_session)]
