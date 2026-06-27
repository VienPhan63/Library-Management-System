from sqlalchemy import select

from models import Reader
from models.reader import ReaderStatus

from .base_repository import BaseRepository


class ReaderRepository(BaseRepository[Reader]):

    def __init__(self, session):
        super().__init__(Reader, session)

    def get_by_email(self, email: str) -> Reader | None:
        stmt = select(Reader).where(Reader.email == email)
        return self.session.scalar(stmt)

    def get_active_readers(self) -> list[Reader]:
        stmt = select(Reader).where(
            Reader.status == ReaderStatus.ACTIVE
        )
        return list(self.session.scalars(stmt))

    def search(self, keyword: str) -> list[Reader]:
        stmt = select(Reader).where(
            Reader.full_name.ilike(f"%{keyword}%")
        )
        return list(self.session.scalars(stmt))