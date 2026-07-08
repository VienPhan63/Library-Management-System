from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.security import verify_password
from database.dependencies import get_db
from models.reader import ReaderStatus
from repositories import LibrarianRepository, ReaderRepository


router = APIRouter(prefix="/auth", tags=["Auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    librarian = LibrarianRepository(db).get_by_email(payload.email)
    if librarian and verify_password(payload.password, librarian.password):
        return {
            "id": librarian.id,
            "user_id": librarian.id,
            "full_name": librarian.full_name,
            "email": librarian.email,
            "role": "librarian",
            "token": librarian.id,
        }

    reader = ReaderRepository(db).get_by_email(payload.email)
    if reader and verify_password(payload.password, reader.password):
        if reader.status == ReaderStatus.BLOCKED:
            raise HTTPException(status_code=403, detail="Reader is blocked")
        return {
            "id": reader.id,
            "user_id": reader.id,
            "full_name": reader.full_name,
            "email": reader.email,
            "role": "reader",
            "token": reader.id,
        }

    raise HTTPException(status_code=401, detail="Invalid Library Card ID (email) or Password")
