from datetime import date, datetime

from pydantic import BaseModel, Field


class ReportCreate(BaseModel):

    report_type: str = Field(
        min_length=1,
        max_length=30
    )

    start_date: date

    end_date: date

    librarian_id: str


class ReportResponse(BaseModel):

    id: str

    report_type: str

    start_date: date
    end_date: date

    total_books: int
    borrowed_books: int

    total_borrows: int
    total_returns: int
    overdue_returns: int

    total_fine_amount: int

    total_cards_issued: int
    active_readers: int

    librarian_id: str

    created_at: datetime | None = None
    updated_at: datetime | None = None


    model_config = {
        "from_attributes": True
    }
