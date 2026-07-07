from datetime import date

from sqlalchemy import Date, ForeignKey, String, Enum as SQLEnum, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from enum import Enum

from models.timestamp_mixin import TimestampMixin
from models.id_mixin import IdMixin

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.librarian import Librarian

class RequestStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class RegistrationRequest(Base, TimestampMixin, IdMixin):
    __tablename__ = "registration_requests"

    full_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    phone_number: Mapped[str] = mapped_column(String(10))
    gender: Mapped[str] = mapped_column(String(10))
    date_of_birth: Mapped[date | None] = mapped_column(Date)
    national_id: Mapped[str | None] = mapped_column(String(20))

    request_date: Mapped[date] = mapped_column(
    DateTime,
    server_default=func.now(),
    )

    status: Mapped[RequestStatus] = mapped_column(SQLEnum(RequestStatus))

    rejection_reason: Mapped[str | None] = mapped_column(String(100))

    librarian_id: Mapped[str | None] = mapped_column(
        ForeignKey("librarians.id")
    )

    librarian: Mapped["Librarian"] = relationship(
        back_populates="registration_requests"
    )
