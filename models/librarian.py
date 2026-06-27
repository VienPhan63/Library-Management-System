from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

from models.timestamp_mixin import TimestampMixin
from models.id_mixin import IdMixin

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.reader import Reader
    from models.borrow_record import BorrowRecord
    from models.book import Book
    from models.report import Report
    from models.registration_request import RegistrationRequest

class Librarian(Base, TimestampMixin, IdMixin):
    __tablename__ = "librarians"

    full_name: Mapped[str] = mapped_column(String(30))
    phone_number: Mapped[str] = mapped_column(String(10))

    books: Mapped[List["Book"]] = relationship(
        back_populates="librarian",
        cascade="all, delete-orphan"
    )

    readers: Mapped[List["Reader"]] = relationship(
        back_populates="librarian"
    )

    borrow_records: Mapped[List["BorrowRecord"]] = relationship(
        back_populates="librarian"
    )

    reports: Mapped[List["Report"]] = relationship(
        back_populates="librarian"
    )

    registration_requests: Mapped[List["RegistrationRequest"]] = relationship(
        back_populates="librarian"
    )