from datetime import date

from database.session import SessionLocal
from reader.reader_api import ReaderAPI
from models import Librarian


def test_api():

    print("Start test reader api")

    session = SessionLocal()
    api = ReaderAPI(session)

    try:
        librarian = Librarian(
            full_name="Nguyen Van A",
            phone_number="0123456789",
            email="admin_reader_test@gmail.com",
            password="123456",
        )

        session.add(librarian)
        session.commit()

        # CREATE
        reader = api.create_reader(
            full_name="Nguyen Van Dat",
            email="dat_api@gmail.com",
            password="123456",
            phone_number="0908888888",
            gender="Male",
            date_of_birth=date(2003, 3, 3),
            librarian_id=librarian.id,
        )

        session.commit()

        print(reader.id)

        # LOGIN FAIL
        try:
            api.login("dat_api@gmail.com", "saimatkhau")
            print("Dang nhap thanh cong")
        except Exception as e:
            print("Login fail:", e)

        # LOGIN SUCCESS
        try:
            login_reader = api.login("dat_api@gmail.com", "123456")
            print("Login success:", login_reader.full_name)
        except Exception as e:
            print(e)

        # GET
        result = api.get_reader(reader.id)
        print(result.full_name)

        # GET ALL
        readers = api.get_all_readers()
        print(f"Total readers: {len(readers)}")

        # ACTIVE
        active = api.get_active_readers()
        print(f"Active readers: {len(active)}")

        # SEARCH
        search = api.search_reader("Dat")
        print(f"Search result: {len(search)}")

        # UPDATE
        api.update_reader(
            reader.id,
            "Nguyen Van Dat Updated",
            "0901111111",
            "Male",
        )

        session.commit()

        updated = api.get_reader(reader.id)
        print(updated.full_name)

        # DELETE
        api.delete_reader(reader.id)
        session.commit()

        print("Reader deleted")
        print("API test passed!")

    finally:
        session.close()


if __name__ == "__main__":
    test_api()