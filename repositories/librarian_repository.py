from sqlalchemy import select

from models import Librarian

from .base_repository import BaseRepository


class LibrarianRepository(BaseRepository[Librarian]):

    def __init__(self, session):
        super().__init__(Librarian, session)

    def get_by_phone(self, phone: str):
        stmt = select(Librarian).where(
            Librarian.phone_number == phone
        )
        return self.session.scalar(stmt)

    def search(self, keyword: str):
        stmt = select(Librarian).where(
            Librarian.full_name.ilike(f"%{keyword}%")
        )
        return list(self.session.scalars(stmt))