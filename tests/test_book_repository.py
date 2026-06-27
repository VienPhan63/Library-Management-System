from database.session import SessionLocal
from models import Book, Librarian
from repositories import BookRepository
from models.book import BookStatus


def test_repository():

    print("Start test product repository")

    session = SessionLocal()

    repo = BookRepository(session)

    try:

        librarian = Librarian(
            full_name="Dương Nguyễn",
            phone_number="0345678900"
        )

        session.add(librarian)
        session.commit()

        # CREATE

        books = [
            Book(
                title="Python Basic",
                author="John",
                publisher="NXB A",
                publish_year=2024,
                category="Programming",
                description="...",
                quantity=10,
                available_quantity=10,
                status=BookStatus.AVAILABLE,
                librarian_id=librarian.id,
            ),
            Book(
                title="Python Advanced",
                author="John",
                publisher="NXB B",
                publish_year=2023,
                category="Programming",
                description="...",
                quantity=5,
                available_quantity=0,
                status=BookStatus.UNAVAILABLE,
                librarian_id=librarian.id,
            ),
        Book(
                title="Java Core",
                author="James",
                publisher="NXB A",
                publish_year=2022,
                category="Programming",
                description="...",
                quantity=8,
                available_quantity=3,
                status=BookStatus.AVAILABLE,
                librarian_id=librarian.id,
            ),
        ]

        for book in books:
            repo.create(book)

        session.commit()

        print(book.id)

        # GET

        result = repo.get_by_id(book.id)

        print(result.title)

        # DELETE

        # repo.delete(result)

        # session.commit()

        print("Repository test passed!")

    finally:

        session.close()


if __name__ == "__main__":

    test_repository()