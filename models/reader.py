from datetime import date

from sqlalchemy import Date, ForeignKey, String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from enum import Enum

from models.timestamp_mixin import TimestampMixin
from models.id_mixin import IdMixin

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.librarian import Librarian
    from models.borrow_record import BorrowRecord
    from models.registration_request import RegistrationRequest

class ReaderStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    BLOCKED = "BLOCKED"

class Reader(Base, TimestampMixin, IdMixin):
    __tablename__ = "readers"

    full_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30))
    phone_number: Mapped[str] = mapped_column(String(10))
    password: Mapped[str] = mapped_column(String(255))
    gender: Mapped[str] = mapped_column(String(10))
    date_of_birth: Mapped[date] = mapped_column(Date)
    status: Mapped[ReaderStatus] = mapped_column(SQLEnum(ReaderStatus))

    librarian_id: Mapped[str] = mapped_column(
        ForeignKey("librarians.id")
    )

    librarian: Mapped["Librarian"] = relationship(
        back_populates="readers"
    )

    borrow_records: Mapped[list["BorrowRecord"]] = relationship(
        back_populates="reader"
    )
