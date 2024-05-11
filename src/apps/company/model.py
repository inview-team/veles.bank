from uuid import UUID, uuid4

from sqlalchemy.orm import mapped_column, Mapped

from src.core.db import Base


class Company(Base):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]
    email: Mapped[str]

