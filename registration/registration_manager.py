from repositories.registration_request_repository import (
    RegistrationRequestRepository
)
from models.registration_request import RequestStatus


class RegistrationManager:

    def __init__(self, session):
        self.repo = RegistrationRequestRepository(session)

    def view_pending_requests(self):
        return self.repo.get_pending_requests()

    def view_request_detail(self, request_id):
        return self.repo.get_by_id(request_id)

    def approve_request(self, request_id):
        request = self.repo.get_by_id(request_id)

        if request is None:
            return False

        request.status = RequestStatus.APPROVED

        self.repo.update()

        return True

    def reject_request(self, request_id, reason):
        request = self.repo.get_by_id(request_id)

        if request is None:
            return False

        request.status = RequestStatus.REJECTED
        request.rejection_reason = reason

        self.repo.update()

        return True