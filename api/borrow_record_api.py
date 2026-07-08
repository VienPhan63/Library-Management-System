from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.dependencies import get_db

from repositories import (
    BookRepository,
    ReaderRepository,
    BorrowRecordRepository
)

from schemas.borrow import (
    BorrowRequest,
    ReturnRequest
)

from models.borrow_record import (
    BorrowRecord,
    BorrowStatus
)

from models.book import BookStatus
from models.reader import ReaderStatus

router = APIRouter(
    prefix="/borrow-record",
    tags=["Borrow Record"]
)

@router.post("/borrow")
def borrow_book(
    request: BorrowRequest,
    db: Session = Depends(get_db)
):

    try:

        book_repo = BookRepository(db)
        reader_repo = ReaderRepository(db)
        borrow_repo = BorrowRecordRepository(db)

        # Check Book Information

        book = book_repo.get_by_id(request.book_id)

        if not book:
            raise HTTPException(
                status_code=404,
                detail="Book not found"
            )

        if book.available_quantity <= 0:
            raise HTTPException(
                status_code=400,
                detail="Book unavailable"
            )

        # Verify Reader Information

        reader = reader_repo.get_by_id(request.reader_id)

        if not reader:
            raise HTTPException(
                status_code=404,
                detail="Reader not found"
            )

        # Check Library Card Status

        if reader.status != ReaderStatus.ACTIVE:
            raise HTTPException(
                status_code=400,
                detail="Reader is not active"
            )

        # Create Loan Record

        borrow_date = date.today()

        due_date = borrow_date + timedelta(days=14)

        record = BorrowRecord(
            borrow_date=borrow_date,
            due_date=due_date,
            status=BorrowStatus.BORROWED,
            book_id=book.id,
            reader_id=reader.id,
            librarian_id=request.librarian_id
        )

        borrow_repo.create(record)

        # Update Book

        book.available_quantity -= 1

        if book.available_quantity == 0:
            book.status = BookStatus.UNAVAILABLE

        db.commit()

        return {
            "message": "Borrow successfully"
        }

    except Exception:

        db.rollback()
        raise

@router.post("/return")
def return_book(
    request: ReturnRequest,
    db: Session = Depends(get_db)
):
    try:

        book_repo = BookRepository(db)
        borrow_repo = BorrowRecordRepository(db)
        reader_repo = ReaderRepository(db)

        # Check Loan Record

        record = borrow_repo.get_by_id(
            request.borrow_record_id
        )

        if record is None:
            raise HTTPException(
                status_code=404,
                detail="Borrow record not found"
            )

        if record.return_date is not None:
            raise HTTPException(
                status_code=400,
                detail="Book already returned"
            )
        # Verify Reader Information

        reader = reader_repo.get_by_id(
            record.reader_id
        )

        if reader is None:
            raise HTTPException(
                status_code=404,
                detail="Reader not found"
            )

        if reader.status != ReaderStatus.ACTIVE:
            raise HTTPException(
                status_code=400,
                detail="Reader is not active"
            )

        # Check Book Condition

        book = book_repo.get_by_id(
            record.book_id
        )

        if book is None:
            raise HTTPException(
                status_code=404,
                detail="Book not found"
            )
        # Calculate Late Fees
    
        today = date.today()

        late_days = 0

        if today > record.due_date:
            late_days = (
                today - record.due_date
            ).days

        fine = late_days * 15000

        # Process Borrowing and Returning Policy Violations

        if request.is_damaged:
            fine += book.price * 0.5

        if request.is_lost:
            fine += book.price * 2

        # Update Borrowing Record

        record.return_date = today
        record.status = BorrowStatus.RETURNED
        # Update Book

        if not request.is_lost:

            book.available_quantity += 1

            if book.available_quantity > 0:
                book.status = BookStatus.AVAILABLE

        db.commit()

        return {
            "message": "Return successfully",
            "late_days": late_days,
            "fine": fine
        }

    except Exception:

        db.rollback()      
        raise