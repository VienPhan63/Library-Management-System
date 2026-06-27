from sqlalchemy import select, or_

from models import Book
from models.book import BookStatus

from .base_repository import BaseRepository


class BookRepository(BaseRepository[Book]):

    def __init__(self, session):
        super().__init__(Book, session)

    def get_by_title(self, title: str) -> list[Book]:
        stmt = select(Book).where(Book.title.ilike(f"%{title}%"))
        return list(self.session.scalars(stmt))

    def get_by_author(self, author: str) -> list[Book]:
        stmt = select(Book).where(Book.author.ilike(f"%{author}%"))
        return list(self.session.scalars(stmt))

    def get_by_category(self, category: str) -> list[Book]:
        stmt = select(Book).where(Book.category.ilike(f"%{category}%"))
        return list(self.session.scalars(stmt))

    def get_available_books(self) -> list[Book]:
        stmt = select(Book).where(
            Book.available_quantity > 0,
            Book.status == BookStatus.AVAILABLE
        )
        return list(self.session.scalars(stmt))

    def search(self, keyword: str) -> list[Book]:
        stmt = (
            select(Book)
            .where(
                or_(
                    Book.title.ilike(f"%{keyword}%"),
                    Book.author.ilike(f"%{keyword}%"),
                    Book.publisher.ilike(f"%{keyword}%")
                )
            )
        )
        return list(self.session.scalars(stmt))