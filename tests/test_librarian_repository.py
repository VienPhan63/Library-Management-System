from database.session import SessionLocal

from models import Librarian
from repositories import LibrarianRepository


def test_repository():
    print("=== Librarian Repository Test ===")

    session = SessionLocal()
    repo = LibrarianRepository(session)

    try:
        # CREATE
        librarian = Librarian(
            full_name="Nguyen Van A",
            phone_number="0123456789"
        )

        repo.create(librarian)
        session.commit()

        print(f"Created: {librarian.id}")

        # GET
        result = repo.get_by_id(librarian.id)

        assert result is not None
        assert result.full_name == "Nguyen Van A"

        print(f"Found: {result.full_name}")

        # EXISTS
        assert repo.exists(librarian.id)

        print("Exists: True")

        # COUNT
        print(f"Total librarians: {repo.count()}")

        # DELETE
        repo.delete(result)
        session.commit()

        print("Deleted successfully")

        assert not repo.exists(librarian.id)

        print("Repository test passed!")

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


if __name__ == "__main__":
    test_repository()