from reader.reader_manager import ReaderManager


class ReaderAPI:

    def __init__(self, session):
        self.manager = ReaderManager(session)

    def get_reader(self, reader_id):
        return self.manager.get_reader(reader_id)

    def get_all_readers(self):
        return self.manager.get_all_readers()

    def get_active_readers(self):
        return self.manager.get_active_readers()

    def search_reader(self, keyword):
        return self.manager.search_reader(keyword)

    def create_reader(
        self,
        full_name,
        email,
        password,
        phone_number,
        gender,
        date_of_birth,
        librarian_id,
    ):
        return self.manager.create_reader(
            full_name,
            email,
            password,
            phone_number,
            gender,
            date_of_birth,
            librarian_id,
        )

    def update_reader(
        self,
        reader_id,
        full_name,
        phone_number,
        gender,
    ):
        return self.manager.update_reader(
            reader_id,
            full_name,
            phone_number,
            gender,
        )

    def delete_reader(self, reader_id):
        return self.manager.delete_reader(reader_id)