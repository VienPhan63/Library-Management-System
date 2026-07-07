from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LibrarianCreate(BaseModel):
    full_name: str
    phone_number: str


class LibrarianUpdate(BaseModel):
    full_name: str | None = None
    phone_number: str | None = None


class LibrarianResponse(BaseModel):
    id: str
    full_name: str
    phone_number: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
