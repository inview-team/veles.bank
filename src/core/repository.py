from typing import Generic, Protocol, Self, Type, TypeVar, cast, get_args

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import BASE_ID, Base

ModelType = TypeVar('ModelType', bound=Base, covariant=True)
ReadSchemaType = TypeVar('ReadSchemaType', bound=BaseModel)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)



class BaseRepositoryProtocol(Protocol[ModelType, ReadSchemaType, CreateSchemaType, UpdateSchemaType]):
    async def get(self: Self, id: BASE_ID | str) -> ReadSchemaType:
        ...

    async def create(self: Self, create_object: CreateSchemaType) -> ReadSchemaType:
        ...

    async def update(self, update_object: UpdateSchemaType) -> ReadSchemaType:
        ...


class BaseRepositoryImpl(Generic[ModelType, ReadSchemaType, CreateSchemaType, UpdateSchemaType]):
    __orig_bases__: 'tuple[Type[BaseRepositoryImpl[ModelType, ReadSchemaType, CreateSchemaType, UpdateSchemaType]]]'

    model_type: Type[ModelType]
    read_schema_type: Type[ReadSchemaType]
    create_schema_type: Type[CreateSchemaType]

    def __init__(self: Self, session: AsyncSession):
        self.session = session

    def __init_subclass__(cls) -> None:
        if not hasattr(cls, '__orig_bases__'):
            raise ValueError('Not implements by BaseImplRepository')
        base_repository_generic, *_ = cls.__orig_bases__
        cls.model_type, cls.read_schema_type, cls.create_schema_type, *_ = cast(
            tuple[Type[ModelType], Type[ReadSchemaType], Type[CreateSchemaType], Type[UpdateSchemaType]],
            get_args(base_repository_generic),
        )
        return super().__init_subclass__()

    async def get(self: Self, id: BASE_ID | str) -> ReadSchemaType:
        async with self.session as s:
            statement = sa.select(self.model_type).where(self.model_type.id == id)
            model = (await s.execute(statement)).scalar_one_or_none()
            if model is None:
                return None
            return self.read_schema_type.model_validate(model, from_attributes=True)

    async def get_by_ids(self: Self, ids: list[BASE_ID | str]) -> list[ReadSchemaType]:
        async with self.session as s:
            statement = sa.select(self.model_type).where(self.model_type.id.in_(ids))
            models = (await s.execute(statement)).scalars().all()
            return [self.read_schema_type.model_validate(model, from_attributes=True) for model in models]

    async def create(self: Self, create_object: CreateSchemaType) -> ReadSchemaType:
        async with self.session as s, s.begin():
            statement = (
                sa.insert(self.model_type).values(**create_object.model_dump(exclude={'id'})).returning(self.model_type)
            )
            model = (await s.execute(statement)).scalar_one()
            return self.read_schema_type.model_validate(model, from_attributes=True)

    async def update(self, update_object: UpdateSchemaType) -> ReadSchemaType:
        async with self.session as s, s.begin():
            pk = update_object.id
            statement = (
                sa.update(self.model_type)
                .where(self.model_type.id == pk)
                .values(update_object.model_dump(exclude={'id'}, exclude_unset=True))
                .returning(self.model_type)
            )
            model = (await s.execute(statement)).scalar_one()
            return self.read_schema_type.model_validate(model, from_attributes=True)
