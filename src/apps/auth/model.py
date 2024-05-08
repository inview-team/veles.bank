from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base


class AuthToken(Base):
    """
    Модель токена авторизации.
    """

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    token: Mapped[str]
    type: Mapped[str]

    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))

