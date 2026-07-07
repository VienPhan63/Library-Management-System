from database.session import SessionLocal

from models import Reader
from repositories import ReaderRepository
from datetime import date

def test_repository():
    print("=== Reader Repository Test ===")

    session = SessionLocal()
    repo = ReaderRepository(session)

    try:
        # CREATE
        reader = Reader(
            full_name="Nguyen Van A",
            phone_number="0123456789",
            email="reader@reader.com",
            password="readerpassword",
            gender="nam",
            date_of_birth=date(2010, 1, 1),
            status="ACTIVE",
            librarian_id="e898c07f-3cc1-4c07-b3ec-8273983dbec4",
        )

        repo.create(reader)
        session.commit()

        print(f"Created: {reader.id}")

        # GET
        result = repo.get_by_id(reader.id)

        assert result is not None
        assert result.full_name == "Nguyen Van A"

        print(f"Found: {result.full_name}")

        # EXISTS
        assert repo.exists(reader.id)

        print("Exists: True")

        # COUNT
        print(f"Total readers: {repo.count()}")

        print("Repository test passed!")

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


if __name__ == "__main__":
    test_repository()