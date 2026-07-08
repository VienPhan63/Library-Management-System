from datetime import date
from pydantic import BaseModel


class ReaderLogin(BaseModel):
    email: str
    password: str


class ReaderResponse(BaseModel):
    id: str
    full_name: str
    email: str
    phone_number: str
    gender: str
    date_of_birth: date

    class Config:
        from_attributes = True