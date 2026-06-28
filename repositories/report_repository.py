from datetime import date

from sqlalchemy import select

from models import Report
from models import BorrowRecord   

from .base_repository import BaseRepository


class ReportRepository(BaseRepository[Report]):

    def __init__(self, session):
        super().__init__(Report, session)

    def get_latest(self):
        stmt = (
            select(Report)
            .order_by(Report.end_date.desc())
            .limit(1)
        )
        return self.session.scalar(stmt)

    def get_between_dates(
        self,
        start_date: date,
        end_date: date
    ):
        stmt = (
            select(Report)
            .where(
                Report.start_date >= start_date,
                Report.end_date <= end_date
            )
        )
        return list(self.session.scalars(stmt))


    def get_total_fine(
        self,
        start_date: date,
        end_date: date
    ) -> int:

        stmt = (
            select(BorrowRecord)
            .where(
                BorrowRecord.return_date != None,
                BorrowRecord.return_date >= start_date,
                BorrowRecord.return_date <= end_date
            )
        )

        records = list(self.session.scalars(stmt))

        total_fine = 0

        for record in records:

           
            if record.return_date > record.due_date:

                overdue_days = (
                    record.return_date -
                    record.due_date
                ).days

                total_fine += overdue_days * 15000

        return total_fine