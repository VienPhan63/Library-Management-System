from repositories.registration_request_repository import (
    RegistrationRequestRepository
)

from models.registration_request import (
    RegistrationRequest,
    RequestStatus,
)


class RegistrationAPI:

    def __init__(self, session):
        self.repo = RegistrationRequestRepository(session)

    def register(
        self,
        full_name,
        email,
        password,
        phone_number,
        gender,
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

        if self.repo.get_by_email(email):
            raise ValueError("Email already exists")

        request = RegistrationRequest(
            full_name=full_name,
            email=email,
            password=password,
            phone_number=phone_number,
            gender=gender,
            status=RequestStatus.PENDING,
        )

        self.repo.create(request)

        return request

    def get_pending_requests(self):
        return self.repo.get_pending_requests()

    def get_request_detail(self, request_id):

        if not request_id:
            raise ValueError("Request ID is required")

        return self.repo.get_by_id(request_id)

    def approve_request(self, request_id):

        if not request_id:
            raise ValueError("Request ID is required")

        request = self.repo.get_by_id(request_id)

        if request is None:
            return False

        if request.status != RequestStatus.PENDING:
            raise ValueError("Request has already been processed")

        request.status = RequestStatus.APPROVED

        self.repo.update()

        return request
    def reject_request(self, request_id, reason):

        if not request_id:
            raise ValueError("Request ID is required")

        if not reason or not reason.strip():
            raise ValueError("Rejection reason is required")

        request = self.repo.get_by_id(request_id)

        if request is None:
            return False

        if request.status != RequestStatus.PENDING:
            raise ValueError("Request has already been processed")

        request.status = RequestStatus.REJECTED
        request.rejection_reason = reason

        self.repo.update()

        return True