from datetime import date

from database.session import SessionLocal
from reader.reader_request import ReaderRequest
from models import Librarian


def test_request():

    print("Start test reader request")

    session = SessionLocal()

    request = ReaderRequest(session)

    try:

        librarian = Librarian(
            full_name="Nguyen Van A",
            phone_number="0123456789",
        )

        session.add(librarian)
        session.commit()

        # CREATE

        reader = request.create_reader(
            full_name="Tran Van Dat",
            email="request@gmail.com",
            password="123456",
            phone_number="0900000000",
            gender="Male",
            date_of_birth=date(2003, 1, 1),
            librarian_id=librarian.id,
        )

        session.commit()

        print(reader.id)

        # GET

        result = request.get_reader(reader.id)

        print(result.full_name)

        # GET ALL

        readers = request.get_all_readers()

        print(f"Total readers: {len(readers)}")

        # ACTIVE

        active = request.get_active_readers()

        print(f"Active readers: {len(active)}")

        # SEARCH

        search = request.search_reader("Dat")

        print(f"Search result: {len(search)}")

        # UPDATE

        request.update_reader(
            reader.id,
            "Tran Van Dat Updated",
            "0999999999",
            "Male",
        )

        session.commit()

        updated = request.get_reader(reader.id)

        print(updated.full_name)

        # DELETE

        request.delete_reader(reader.id)

        session.commit()

        print("Reader deleted")

        print("Request test passed!")

    finally:

        session.close()


if __name__ == "__main__":
    test_request()