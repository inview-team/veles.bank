from uuid import UUID

from sqlalchemy.orm import Mapped

from src.core.db import Base


class User(Base):
    """
    Модель пользователя.
    """

    id: Mapped[UUID]
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
