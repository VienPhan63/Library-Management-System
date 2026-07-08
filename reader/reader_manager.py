from csv import reader

from repositories.reader_repository import ReaderRepository
from models.reader import Reader, ReaderStatus


class ReaderManager:

    def __init__(self, session):
        self.repo = ReaderRepository(session)

    def get_reader(self, reader_id):
        if not reader_id:
            raise ValueError("Reader ID is required")

        return self.repo.get_by_id(reader_id)

    def get_all_readers(self):
        return self.repo.get_all()

    def get_active_readers(self):
        return self.repo.get_active_readers()

    def search_reader(self, keyword):
        if not keyword:
            return []

        return self.repo.search(keyword)

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
        if not full_name or not full_name.strip():
            raise ValueError("Full name is required")

        if not email or not email.strip():
            raise ValueError("Email is required")

        if not password or not password.strip():
            raise ValueError("Password is required")

        if not phone_number or not phone_number.strip():
            raise ValueError("Phone number is required")

        if not gender or not gender.strip():
            raise ValueError("Gender is required")

        if not date_of_birth:
            raise ValueError("Date of birth is required")

        if self.repo.get_by_email(email):
            raise ValueError("Email already exists")

        reader = Reader(
            full_name=full_name,
            email=email,
            password=password,
            phone_number=phone_number,
            gender=gender,
            date_of_birth=date_of_birth,
            status=ReaderStatus.ACTIVE,
            librarian_id=librarian_id,
        )

        self.repo.create(reader)

        return reader

    def update_reader(
        self,
        reader_id,
        full_name,
        phone_number,
        gender,
    ):
        if not reader_id:
            raise ValueError("Reader ID is required")

        reader = self.repo.get_by_id(reader_id)

        if reader is None:
            return False

        if not full_name or not full_name.strip():
            raise ValueError("Full name is required")

        if not phone_number or not phone_number.strip():
            raise ValueError("Phone number is required")

        if not gender or not gender.strip():
            raise ValueError("Gender is required")

        reader.full_name = full_name
        reader.phone_number = phone_number
        reader.gender = gender

        self.repo.update()

        return reader

    def delete_reader(self, reader_id):
    
        if not reader_id:
            raise ValueError("Reader ID is required")

        reader = self.repo.get_by_id(reader_id)

        if reader is None:
            raise ValueError("Reader not found")

        self.repo.delete(reader)

        return True

    def login(self, email, password):
        if not email or not email.strip():
            raise ValueError("Email is required")

        if not password or not password.strip():
            raise ValueError("Password is required")

        reader = self.repo.get_by_email(email)

        if reader is None:
            raise ValueError("Email does not exist")

        if reader.password != password:
            raise ValueError("Incorrect password")

        if reader.status != ReaderStatus.ACTIVE:
            raise ValueError("Reader account is not active")

        return reader