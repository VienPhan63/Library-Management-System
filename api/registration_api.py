from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.dependencies import get_db

from repositories import RegistrationRequestRepository

from schemas.registration import RegisterRequest

from models import RegistrationRequest
from models.registration_request import RequestStatus

router = APIRouter(
    prefix="/registrations",
    tags=["Registration"]
)

@router.post("/")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):

    repo = RegistrationRequestRepository(db)

    if repo.get_by_email(request.email):

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    registration = RegistrationRequest(

        full_name=request.full_name,

        email=request.email,

        password=request.password,

        phone_number=request.phone_number,

        gender=request.gender,

        status=RequestStatus.PENDING

    )

    repo.create(registration)

    db.commit()

    return registration

@router.get("/pending")
def get_pending_requests(
    db: Session = Depends(get_db)
):

    repo = RegistrationRequestRepository(db)

    return repo.get_pending_requests()