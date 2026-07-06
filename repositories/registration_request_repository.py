from sqlalchemy import select, func

from models import RegistrationRequest
from models.registration_request import RequestStatus

from .base_repository import BaseRepository


class RegistrationRequestRepository(
    BaseRepository[RegistrationRequest]
):

    def __init__(self, session):
        super().__init__(RegistrationRequest, session)

    def get_pending_requests(self):
        stmt = select(RegistrationRequest).where(
            RegistrationRequest.status == RequestStatus.PENDING
        )
        return list(self.session.scalars(stmt))

    def get_by_email(self, email: str):
        stmt = select(RegistrationRequest).where(
            RegistrationRequest.email == email
        )
        return self.session.scalar(stmt)

    def get_by_status(self, status: RequestStatus):
        stmt = select(RegistrationRequest).where(
            RegistrationRequest.status == status
        )
        return list(self.session.scalars(stmt))
    
    def count_pending(self):
        stmt = (select(func.count()).where(
            RegistrationRequest.status == RequestStatus.PENDING
        ))
        return self.session.scalar(stmt)