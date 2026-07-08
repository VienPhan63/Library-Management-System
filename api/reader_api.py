from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.dependencies import get_db
from reader.reader_API import ReaderAPI

router = APIRouter(
    prefix="/reader",
    tags=["Reader"]
)


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    try:
        api = ReaderAPI(db)

        reader = api.login(
            data.email,
            data.password,
        )

        return {
            "success": True,
            "reader_id": reader.id,
            "full_name": reader.full_name,
            "email": reader.email,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )