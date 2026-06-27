from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from enum import Enum
from sqlalchemy import Enum as SQLEnum

from models.timestamp_mixin import TimestampMixin
from models.id_mixin import IdMixin

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.reader import Reader
    from models.librarian import Librarian
    from models.book import Book

class BorrowStatus(str, Enum):
    BORROWED = "BORROWED"
    RETURNED = "RETURNED"
    OVERDUE = "OVERDUE"

class BorrowRecord(Base, TimestampMixin, IdMixin):
    __tablename__ = "borrow_records"

    borrow_date: Mapped[date] = mapped_column(Date)

    due_date: Mapped[date] = mapped_column(Date)

    return_date: Mapped[date | None] = mapped_column(Date)

    status: Mapped[BorrowStatus] = mapped_column(SQLEnum(BorrowStatus))

    reader_id: Mapped[str] = mapped_column(
        ForeignKey("readers.id")
    )

    book_id: Mapped[str] = mapped_column(
        ForeignKey("books.id")
    )

    librarian_id: Mapped[str] = mapped_column(
        ForeignKey("librarians.id")
    )

    reader: Mapped["Reader"] = relationship(
        back_populates="borrow_records"
    )

    book: Mapped["Book"] = relationship(
        back_populates="borrow_records"
    )

    librarian: Mapped["Librarian"] = relationship(
        back_populates="borrow_records"
    )