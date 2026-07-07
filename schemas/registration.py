
from datetime import date, datetime

from pydantic import BaseModel

from models.registration_request import RequestStatus

class RegisterRequest(BaseModel):

    full_name: str
    email: str
    password: str
    phone_number: str
    gender: str
    date_of_birth: date | None = None
    national_id: str | None = None


class RejectRegistrationRequest(BaseModel):
    reason: str


class RegistrationResponse(BaseModel):
    id: str
    full_name: str
    email: str
    phone_number: str
    gender: str
    date_of_birth: date | None = None
    national_id: str | None = None
    request_date: datetime | None = None
    status: RequestStatus
    rejection_reason: str | None = None
    librarian_id: str | None = None

    model_config = {
        "from_attributes": True
    }
