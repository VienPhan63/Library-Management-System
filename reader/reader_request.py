from reader.reader_api import ReaderAPI


class ReaderRequest:

    def __init__(self, session):
        self.api = ReaderAPI(session)

    def get_reader(self, reader_id):
        return self.api.get_reader(reader_id)

    def get_all_readers(self):
        return self.api.get_all_readers()

    def get_active_readers(self):
        return self.api.get_active_readers()

    def search_reader(self, keyword):
        return self.api.search_reader(keyword)

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
        return self.api.create_reader(
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
        return self.api.update_reader(
            reader_id,
            full_name,
            phone_number,
            gender,
        )

    def delete_reader(self, reader_id):
        return self.api.delete_reader(reader_id)