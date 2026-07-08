from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from models.id_mixin import IdMixin
from models.timestamp_mixin import TimestampMixin


class Category(Base, TimestampMixin, IdMixin):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str | None] = mapped_column(String(255))
