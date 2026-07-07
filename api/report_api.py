from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import distinct, func, select
from sqlalchemy.orm import Session

from database.dependencies import get_db
from models import Book, BorrowRecord, Reader, RegistrationRequest
from models.borrow_record import BorrowStatus
from models.reader import ReaderStatus
from models.registration_request import RequestStatus


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

FINE_PER_DAY = 15000


def _count(db: Session, stmt) -> int:
    return db.scalar(stmt) or 0


@router.get("/summary")
def get_report_summary(db: Session = Depends(get_db)):
    total_titles = _count(db, select(func.count()).select_from(Book))
    total_categories = _count(db, select(func.count(distinct(Book.category))))
    total_stock = _count(db, select(func.coalesce(func.sum(Book.quantity), 0)))
    available_stock = _count(db, select(func.coalesce(func.sum(Book.available_quantity), 0)))

    currently_borrowed = max(total_stock - available_stock, 0)

    total_borrows = _count(db, select(func.count()).select_from(BorrowRecord))
    total_returns = _count(
        db,
        select(func.count()).where(BorrowRecord.status == BorrowStatus.RETURNED)
    )
    overdue_returns = _count(
        db,
        select(func.count()).where(
            BorrowRecord.return_date.is_not(None),
            BorrowRecord.return_date > BorrowRecord.due_date
        )
    )
    active_readers = _count(
        db,
        select(func.count()).where(Reader.status == ReaderStatus.ACTIVE)
    )
    total_cards_issued = _count(
        db,
        select(func.count()).where(
            RegistrationRequest.status == RequestStatus.APPROVED
        )
    )

    returned_records = list(
        db.scalars(
            select(BorrowRecord).where(BorrowRecord.return_date.is_not(None))
        )
    )

    total_fine_amount = 0
    for record in returned_records:
        if record.return_date and record.return_date > record.due_date:
            total_fine_amount += (
                record.return_date - record.due_date
            ).days * FINE_PER_DAY

    active_borrow_records = _count(
        db,
        select(func.count()).where(BorrowRecord.status == BorrowStatus.BORROWED)
    )
    overdue_active_records = _count(
        db,
        select(func.count()).where(
            BorrowRecord.status == BorrowStatus.BORROWED,
            BorrowRecord.due_date < date.today()
        )
    )

    return {
        "total_titles": total_titles,
        "total_categories": total_categories,
        "total_stock": total_stock,
        "available_stock": available_stock,
        "currently_borrowed": currently_borrowed,
        "active_borrow_records": active_borrow_records,
        "total_borrows": total_borrows,
        "total_returns": total_returns,
        "overdue_returns": overdue_returns,
        "overdue_active_records": overdue_active_records,
        "total_fine_amount": total_fine_amount,
        "total_cards_issued": total_cards_issued,
        "active_readers": active_readers
    }
