

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from enum import Enum
from sqlalchemy import Enum as SQLEnum

from models.timestamp_mixin import TimestampMixin
from models.id_mixin import IdMixin

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.borrow_record import BorrowRecord
    from models.librarian import Librarian

class BookStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    ARCHIVED = "ARCHIVED"

class Book(Base, TimestampMixin, IdMixin):
    __tablename__ = "books"

    title: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(30))
    publisher: Mapped[str] = mapped_column(String(30))

    publish_year: Mapped[int] = mapped_column(Integer)

    category: Mapped[str] = mapped_column(String(30))

    description: Mapped[str] = mapped_column(String(100))

    quantity: Mapped[int] = mapped_column(Integer)

    available_quantity: Mapped[int] = mapped_column(Integer)

    status: Mapped[BookStatus] = mapped_column(SQLEnum(BookStatus))

    librarian_id: Mapped[str] = mapped_column(
        ForeignKey("librarians.id")
    )

    librarian: Mapped["Librarian"] = relationship(
        back_populates="books"
    )

    borrow_records: Mapped[list["BorrowRecord"]] = relationship(
        back_populates="book"
    )

