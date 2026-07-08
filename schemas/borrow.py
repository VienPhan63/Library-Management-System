from datetime import date

from pydantic import BaseModel

from models.borrow_record import BorrowStatus


class BorrowRequest(BaseModel):

    reader_id: str
    book_id: str
    librarian_id: str | None = None
    borrow_date: date | None = None
    due_date: date | None = None


class ReturnRequest(BaseModel):

    borrow_record_id: str
    is_damaged: bool = False
    is_lost: bool = False
    return_date: date | None = None
    book_condition: str | None = None


class BorrowRecordResponse(BaseModel):

    id: str
    borrow_date: date
    due_date: date
    return_date: date | None = None

    status: BorrowStatus

    reader_id: str
    book_id: str
    librarian_id: str

    model_config = {
        "from_attributes": True
    }
