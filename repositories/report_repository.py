from datetime import date

from sqlalchemy import select

from models import Report

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