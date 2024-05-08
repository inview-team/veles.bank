from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base, BASE_ID


class Wallet(Base):
    """
    Модель банковского счета.
    """

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    balance: Mapped[float] = mapped_column(default=0.0)
    type: Mapped[str]
    number: Mapped[str]
    status: Mapped[bool]
    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
