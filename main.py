from database.session import SessionLocal
from registration.registration_api import RegistrationAPI

session = SessionLocal()
api = RegistrationAPI(session)

print(api.get_pending_requests())