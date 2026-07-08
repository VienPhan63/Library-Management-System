from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, select
from sqlalchemy.orm import Session, joinedload

from api.librarian_auth import get_current_librarian
from database.dependencies import get_db
from models import BorrowRecord, Fine, Librarian, LibraryCard, LibraryCardStatus
from models.book import BookStatus
from models.borrow_record import BorrowStatus
from models.reader import ReaderStatus
from repositories import BookRepository, BorrowRecordRepository, ReaderRepository
from schemas.borrow import BorrowRequest, ReturnRequest


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
        "book_price": record.book.price if record.book else 0,
        "borrow_date": record.borrow_date,
        "due_date": record.due_date,
        "return_date": record.return_date,
        "fine_amount": _fine_amount(record),
        "status": _record_status(record),
        "reader_id": record.reader_id,
    }


@router.post("/", status_code=201)
def create_borrow_record(
    payload: BorrowRequest,
    librarian: Librarian = Depends(get_current_librarian),
    db: Session = Depends(get_db),
):
    book_repo = BookRepository(db)
    reader_repo = ReaderRepository(db)
    borrow_repo = BorrowRecordRepository(db)

    card = db.scalar(select(LibraryCard).where(LibraryCard.card_code == payload.reader_id))
    if card and card.status != LibraryCardStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Library card is not active")

    reader = card.reader if card else reader_repo.get_by_id(payload.reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    if reader.status != ReaderStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Reader is not active")

    book = book_repo.get_by_id(payload.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.available_quantity <= 0:
        raise HTTPException(status_code=400, detail="All copies of this book are currently borrowed")

    borrow_date = payload.borrow_date or date.today()
    due_date = payload.due_date or borrow_date

    record = BorrowRecord(
        borrow_date=borrow_date,
        due_date=due_date,
        return_date=None,
        status=BorrowStatus.BORROWED,
        book_id=book.id,
        reader_id=reader.id,
        librarian_id=payload.librarian_id or librarian.id,
    )
    borrow_repo.create(record)

    book.available_quantity -= 1
    book.status = BookStatus.AVAILABLE if book.available_quantity > 0 else BookStatus.UNAVAILABLE

    db.commit()
    db.refresh(record)

    return {
        "message": "Borrow record created successfully",
        "record": _serialize_record(record),
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


@router.get("/active")
def get_active_borrow_records(
    reader_id: str = Query(),
    librarian: Librarian = Depends(get_current_librarian),
    db: Session = Depends(get_db),
):
    card = db.scalar(select(LibraryCard).where(LibraryCard.card_code == reader_id))
    resolved_reader_id = card.reader_id if card else reader_id
    records = db.scalars(
        select(BorrowRecord)
        .options(joinedload(BorrowRecord.book))
        .where(
            BorrowRecord.reader_id == resolved_reader_id,
            BorrowRecord.status.in_([BorrowStatus.BORROWED, BorrowStatus.OVERDUE]),
        )
        .order_by(desc(BorrowRecord.borrow_date))
    )
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


@router.get("/{borrow_record_id}")
def get_borrow_record(
    borrow_record_id: str,
    db: Session = Depends(get_db),
):
    record = db.scalar(
        select(BorrowRecord)
        .options(joinedload(BorrowRecord.book))
        .where(BorrowRecord.id == borrow_record_id)
    )
    if not record:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    return _serialize_record(record)


@router.patch("/{borrow_record_id}/return")
def return_borrow_record(
    borrow_record_id: str,
    payload: ReturnRequest,
    librarian: Librarian = Depends(get_current_librarian),
    db: Session = Depends(get_db),
):
    record = db.scalar(
        select(BorrowRecord)
        .options(joinedload(BorrowRecord.book))
        .where(BorrowRecord.id == borrow_record_id)
    )
    if not record:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    if record.status not in [BorrowStatus.BORROWED, BorrowStatus.OVERDUE]:
        raise HTTPException(status_code=400, detail="Borrow record already returned")

    condition = (payload.book_condition or "").upper()
    is_damaged = payload.is_damaged or condition == "DAMAGED"
    is_lost = payload.is_lost or condition == "LOST"
    return_date = payload.return_date or date.today()

    overdue_days = max((return_date - record.due_date).days, 0)
    overdue_fine = overdue_days * FINE_PER_DAY
    compensation = 0
    reasons = []

    if overdue_fine:
        reasons.append("OVERDUE")
    if is_damaged:
        compensation = int(record.book.price * 0.5)
        reasons.append("DAMAGED")
    if is_lost:
        compensation = int(record.book.price * 2)
        reasons.append("LOST")

    total_fine = overdue_fine + compensation

    record.return_date = return_date
    record.status = BorrowStatus.RETURNED

    if not is_lost:
        record.book.available_quantity += 1
        record.book.status = BookStatus.AVAILABLE if record.book.available_quantity > 0 else BookStatus.UNAVAILABLE

    if total_fine > 0:
        db.add(Fine(
            borrow_record_id=record.id,
            reader_id=record.reader_id,
            book_id=record.book_id,
            reason=", ".join(reasons),
            amount=total_fine,
            paid_status="PAID",
            paid_at=datetime.now(),
        ))

    db.commit()

    return {
        "message": "Return processed successfully",
        "borrow_record_id": record.id,
        "overdue_days": overdue_days,
        "fine": total_fine,
    }
