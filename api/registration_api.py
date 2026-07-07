from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.dependencies import get_db

from repositories import RegistrationRequestRepository

from schemas.registration import (
    RegisterRequest,
    RegistrationResponse,
    RejectRegistrationRequest,
)

from models import RegistrationRequest
from models.registration_request import RequestStatus

router = APIRouter(
    prefix="/registrations",
    tags=["Registration"]
)

@router.post("/", response_model=RegistrationResponse)
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

@router.get("/pending", response_model=list[RegistrationResponse])
def get_pending_requests(
    db: Session = Depends(get_db)
):

    repo = RegistrationRequestRepository(db)

    return repo.get_pending_requests()


@router.get("/{request_id}", response_model=RegistrationResponse)
def get_request_detail(
    request_id: str,
    db: Session = Depends(get_db)
):

    repo = RegistrationRequestRepository(db)

    request = repo.get_by_id(request_id)

    if not request:
        raise HTTPException(
            status_code=404,
            detail="Registration request not found"
        )

    return request


@router.patch("/{request_id}/approve", response_model=RegistrationResponse)
def approve_request(
    request_id: str,
    db: Session = Depends(get_db)
):

    repo = RegistrationRequestRepository(db)

    request = repo.get_by_id(request_id)

    if not request:
        raise HTTPException(
            status_code=404,
            detail="Registration request not found"
        )

    if request.status != RequestStatus.PENDING:
        raise HTTPException(
            status_code=400,
            detail="Request has already been processed"
        )

    request.status = RequestStatus.APPROVED
    request.rejection_reason = None

    db.commit()
    db.refresh(request)

    return request


@router.patch("/{request_id}/reject", response_model=RegistrationResponse)
def reject_request(
    request_id: str,
    payload: RejectRegistrationRequest,
    db: Session = Depends(get_db)
):

    reason = payload.reason.strip()

    if not reason:
        raise HTTPException(
            status_code=400,
            detail="Rejection reason is required"
        )

    repo = RegistrationRequestRepository(db)

    request = repo.get_by_id(request_id)

    if not request:
        raise HTTPException(
            status_code=404,
            detail="Registration request not found"
        )

    if request.status != RequestStatus.PENDING:
        raise HTTPException(
            status_code=400,
            detail="Request has already been processed"
        )

    request.status = RequestStatus.REJECTED
    request.rejection_reason = reason

    db.commit()
    db.refresh(request)

    return request
