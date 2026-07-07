from datetime import date

from database.session import SessionLocal
from models import Reader, Librarian
from models.reader import ReaderStatus
from repositories import ReaderRepository


def test_repository():

    print("Start test reader repository")

    session = SessionLocal()

    repo = ReaderRepository(session)

    try:

        librarian = Librarian(
            full_name="Nguyen Van A",
            phone_number="0123456789",
        )

        session.add(librarian)
        session.commit()

        # CREATE

        readers = [
            Reader(
                full_name="Tran Van Dat",
                email="dat1@gmail.com",
                password="123456",
                phone_number="0900000001",
                gender="Male",
                date_of_birth=date(2003, 1, 1),
                status=ReaderStatus.ACTIVE,
                librarian_id=librarian.id,
            ),
            Reader(
                full_name="Le Thi Lan",
                email="lan@gmail.com",
                password="123456",
                phone_number="0900000002",
                gender="Female",
                date_of_birth=date(2002, 5, 10),
                status=ReaderStatus.INACTIVE,
                librarian_id=librarian.id,
            ),
            Reader(
                full_name="Pham Van B",
                email="b@gmail.com",
                password="123456",
                phone_number="0900000003",
                gender="Male",
                date_of_birth=date(2001, 9, 20),
                status=ReaderStatus.ACTIVE,
                librarian_id=librarian.id,
            ),
        ]

        for reader in readers:
            repo.create(reader)

        session.commit()

        print(reader.id)

        # GET BY ID

        result = repo.get_by_id(reader.id)

        print(result.full_name)

        # GET ACTIVE READERS

        active_readers = repo.get_active_readers()

        print(f"Active readers: {len(active_readers)}")

        # SEARCH

        search_result = repo.search("Dat")

        print(f"Search result: {len(search_result)}")

        # DELETE (nếu muốn test thì bỏ comment)

        # repo.delete(result)
        # session.commit()

        print("Repository test passed!")

    finally:

        session.close()


if __name__ == "__main__":

    test_repository()