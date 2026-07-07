from datetime import date

from database.session import SessionLocal
from reader.reader_manager import ReaderManager
from models import Librarian


def test_manager():

    print("Start test reader manager")

    session = SessionLocal()

    manager = ReaderManager(session)

    try:

        librarian = Librarian(
            full_name="Nguyen Van A",
            phone_number="0123456789",
        )

        session.add(librarian)
        session.commit()

        # CREATE

        reader = manager.create_reader(
            full_name="Tran Van Dat",
            email="dat@gmail.com",
            password="123456",
            phone_number="0901234567",
            gender="Male",
            date_of_birth=date(2003, 1, 1),
            librarian_id=librarian.id,
        )

        session.commit()

        print(reader.id)

        # GET

        result = manager.get_reader(reader.id)

        print(result.full_name)

        # GET ALL

        readers = manager.get_all_readers()

        print(f"Total readers: {len(readers)}")

        # ACTIVE

        active = manager.get_active_readers()

        print(f"Active readers: {len(active)}")

        # SEARCH

        search = manager.search_reader("Dat")

        print(f"Search result: {len(search)}")

        # UPDATE

        manager.update_reader(
            reader.id,
            "Tran Van Dat Updated",
            "0999999999",
            "Male",
        )

        session.commit()

        updated = manager.get_reader(reader.id)

        print(updated.full_name)

        # DELETE

        manager.delete_reader(reader.id)

        session.commit()

        print("Reader deleted")

        print("Manager test passed!")

    finally:

        session.close()


if __name__ == "__main__":

    test_manager()