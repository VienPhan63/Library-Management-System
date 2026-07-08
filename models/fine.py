from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from models.id_mixin import IdMixin
from models.timestamp_mixin import TimestampMixin


class Fine(Base, TimestampMixin, IdMixin):
    __tablename__ = "fines"

    borrow_record_id: Mapped[str] = mapped_column(ForeignKey("borrow_records.id"))
    reader_id: Mapped[str] = mapped_column(ForeignKey("readers.id"))
    book_id: Mapped[str] = mapped_column(ForeignKey("books.id"))
    reason: Mapped[str] = mapped_column(String(100))
    amount: Mapped[int] = mapped_column(Integer)
    paid_status: Mapped[str] = mapped_column(String(20), default="PAID")
    paid_at: Mapped[datetime | None] = mapped_column(DateTime)

    borrow_record = relationship("BorrowRecord")
