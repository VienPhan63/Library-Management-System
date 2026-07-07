from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, select
from sqlalchemy.orm import Session, joinedload

from database.dependencies import get_db
from models import BorrowRecord
from models.borrow_record import BorrowStatus


FINE_PER_DAY = 15000

router = APIRouter(
    prefix="/borrow-records",
    tags=["Borrow Records"],
)


def _fine_amount(record: BorrowRecord) -> int:
    end_date = record.return_date or date.today()
    if end_date <= record.due_date:
        return 0
    return (end_date - record.due_date).days * FINE_PER_DAY


def _record_status(record: BorrowRecord) -> str:
    if record.status == BorrowStatus.BORROWED and record.due_date < date.today():
        return "OVERDUE"
    return record.status.value


def _serialize_record(record: BorrowRecord) -> dict:
    return {
        "id": record.id,
        "book_id": record.book_id,
        "book_title": record.book.title if record.book else "",
        "borrow_date": record.borrow_date,
        "due_date": record.due_date,
        "return_date": record.return_date,
        "fine_amount": _fine_amount(record),
        "status": _record_status(record),
        "reader_id": record.reader_id,
    }


@router.get("/")
def get_borrow_records(
    reader_id: str | None = Query(default=None),
    keyword: str = Query(default=""),
    db: Session = Depends(get_db),
):
    stmt = (
        select(BorrowRecord)
        .options(joinedload(BorrowRecord.book))
        .order_by(desc(BorrowRecord.borrow_date))
    )

    if reader_id:
        stmt = stmt.where(BorrowRecord.reader_id == reader_id)

    records = list(db.scalars(stmt))

    if keyword.strip():
        normalized = keyword.strip().lower()
        records = [
            record for record in records
            if normalized in " ".join(
                [
                    record.id,
                    record.book_id,
                    record.book.title if record.book else "",
                    record.borrow_date.isoformat(),
                    record.due_date.isoformat(),
                    record.return_date.isoformat() if record.return_date else "",
                    record.status.value,
                ]
            ).lower()
        ]

    return [_serialize_record(record) for record in records]


@router.get("/summary")
def get_borrow_summary(
    reader_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    stmt = select(BorrowRecord)
    if reader_id:
        stmt = stmt.where(BorrowRecord.reader_id == reader_id)

    records = list(db.scalars(stmt))
    currently_borrowed = [
        record for record in records
        if record.status == BorrowStatus.BORROWED
    ]

    return {
        "total_borrows": len(records),
        "currently_borrowed": len(currently_borrowed),
        "overdue_books": sum(
            1 for record in currently_borrowed
            if record.due_date < date.today()
        ),
        "total_fines": sum(_fine_amount(record) for record in records),
    }
