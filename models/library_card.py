from enum import Enum

from sqlalchemy import Enum as SQLEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from models.id_mixin import IdMixin
from models.timestamp_mixin import TimestampMixin


class LibraryCardStatus(str, Enum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    INACTIVE = "INACTIVE"


class LibraryCard(Base, TimestampMixin, IdMixin):
    __tablename__ = "library_cards"

    card_code: Mapped[str] = mapped_column(String(36), unique=True, index=True)
    status: Mapped[LibraryCardStatus] = mapped_column(
        SQLEnum(LibraryCardStatus),
        default=LibraryCardStatus.ACTIVE,
    )
    reader_id: Mapped[str] = mapped_column(ForeignKey("readers.id"), unique=True)

    reader = relationship("Reader")
