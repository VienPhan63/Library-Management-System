from datetime import date

from sqlalchemy import select

from models import BorrowRecord
from models.borrow_record import BorrowStatus

from .base_repository import BaseRepository


class BorrowRecordRepository(BaseRepository[BorrowRecord]):

    def __init__(self, session):
        super().__init__(BorrowRecord, session)

    def get_by_reader(self, reader_id: int):
        stmt = select(BorrowRecord).where(
            BorrowRecord.reader_id == reader_id
        )
        return list(self.session.scalars(stmt))

    def get_by_book(self, book_id: int):
        stmt = select(BorrowRecord).where(
            BorrowRecord.book_id == book_id
        )
        return list(self.session.scalars(stmt))

    def get_active_records(self):
        stmt = select(BorrowRecord).where(
            BorrowRecord.status == BorrowStatus.BORROWED
        )
        return list(self.session.scalars(stmt))

    def get_overdue_records(self):
        stmt = select(BorrowRecord).where(
            BorrowRecord.due_date < date.today(),
            BorrowRecord.status == BorrowStatus.BORROWED
        )
        return list(self.session.scalars(stmt))