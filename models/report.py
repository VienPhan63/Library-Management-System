from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

from models.timestamp_mixin import TimestampMixin
from models.id_mixin import IdMixin

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.librarian import Librarian

class Report(Base, TimestampMixin, IdMixin):
    __tablename__ = "reports"

    report_type: Mapped[str] = mapped_column(String(30))

    start_date: Mapped[date] = mapped_column(Date)

    end_date: Mapped[date] = mapped_column(Date)

    total_books: Mapped[int] = mapped_column(Integer)

    borrowed_books: Mapped[int] = mapped_column(Integer)

    total_borrows: Mapped[int] = mapped_column(Integer)

    total_returns: Mapped[int] = mapped_column(Integer)

    overdue_returns: Mapped[int] = mapped_column(Integer)

    total_fine_amount: Mapped[int] = mapped_column(Integer)

    total_cards_issued: Mapped[int] = mapped_column(Integer)

    active_readers: Mapped[int] = mapped_column(Integer)

    librarian_id: Mapped[str] = mapped_column(
        ForeignKey("librarians.id")
    )

    librarian: Mapped["Librarian"] = relationship(
        back_populates="reports"
    )