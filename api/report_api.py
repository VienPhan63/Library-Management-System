from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from api.librarian_auth import get_current_librarian
from database.dependencies import get_db

from models import Book, BorrowRecord, Fine, Librarian, Report
from models.borrow_record import BorrowStatus
from models.reader import Reader, ReaderStatus

from repositories import (
    ReportRepository,
    BookRepository,
    BorrowRecordRepository,
    ReaderRepository,
)

from schemas.report import (
    ReportCreate,
    ReportResponse,
)


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.post("/", response_model=ReportResponse)
def create_report(
    request: ReportCreate,
    librarian: Librarian = Depends(get_current_librarian),
    db: Session = Depends(get_db)
):

    report_repo = ReportRepository(db)
    book_repo = BookRepository(db)
    borrow_repo = BorrowRecordRepository(db)
    reader_repo = ReaderRepository(db)


    total_books = book_repo.count()


    borrowed_books = borrow_repo.count_borrowing()


    total_borrows = borrow_repo.count()


    total_returns = borrow_repo.count_returned()


    overdue_returns = len(
        borrow_repo.get_overdue_records()
    )


    total_fine_amount = report_repo.get_total_fine(
        start_date=request.start_date,
        end_date=request.end_date
    )


    total_cards_issued = reader_repo.count()


    active_readers = len(
        reader_repo.get_active_readers()
    )


    report = Report(

        report_type=request.report_type,

        start_date=request.start_date,

        end_date=request.end_date,

        total_books=total_books,

        borrowed_books=borrowed_books,

        total_borrows=total_borrows,

        total_returns=total_returns,

        overdue_returns=overdue_returns,

        total_fine_amount=total_fine_amount,

        total_cards_issued=total_cards_issued,

        active_readers=active_readers,

        librarian_id=request.librarian_id or librarian.id

    )


    report_repo.create(report)

    db.commit()

    db.refresh(report)


    return report


@router.get("/summary")
def get_report_summary(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    librarian: Librarian = Depends(get_current_librarian),
    db: Session = Depends(get_db),
):
    borrow_stmt = select(BorrowRecord)
    fine_stmt = select(func.coalesce(func.sum(Fine.amount), 0))
    if start_date:
        borrow_stmt = borrow_stmt.where(BorrowRecord.borrow_date >= start_date)
        fine_stmt = fine_stmt.where(func.date(Fine.created_at) >= start_date)
    if end_date:
        borrow_stmt = borrow_stmt.where(BorrowRecord.borrow_date <= end_date)
        fine_stmt = fine_stmt.where(func.date(Fine.created_at) <= end_date)

    records = list(db.scalars(borrow_stmt))
    borrowed_books = sum(1 for record in records if record.status == BorrowStatus.BORROWED)
    returned_records = [record for record in records if record.status == BorrowStatus.RETURNED]
    overdue_returns = sum(
        1
        for record in returned_records
        if record.return_date and record.return_date > record.due_date
    )

    top_book_row = db.execute(
        select(BorrowRecord.book_id, Book.title, func.count(BorrowRecord.id).label("times"))
        .join(Book, Book.id == BorrowRecord.book_id)
        .group_by(BorrowRecord.book_id, Book.title)
        .order_by(func.count(BorrowRecord.id).desc())
    ).first()
    top_reader_row = db.execute(
        select(BorrowRecord.reader_id, Reader.full_name, func.count(BorrowRecord.id).label("times"))
        .join(Reader, Reader.id == BorrowRecord.reader_id)
        .group_by(BorrowRecord.reader_id, Reader.full_name)
        .order_by(func.count(BorrowRecord.id).desc())
    ).first()

    return {
        "total_books": db.scalar(select(func.count(Book.id))) or 0,
        "borrowed_books": borrowed_books,
        "total_borrows": len(records),
        "total_returns": len(returned_records),
        "overdue_returns": overdue_returns,
        "total_fine_amount": int(db.scalar(fine_stmt) or 0),
        "total_cards_issued": db.scalar(select(func.count(Reader.id))) or 0,
        "active_readers": db.scalar(
            select(func.count(Reader.id)).where(Reader.status == ReaderStatus.ACTIVE)
        ) or 0,
        "most_borrowed_book": {
            "book_id": top_book_row[0],
            "title": top_book_row[1],
            "times": top_book_row[2],
        } if top_book_row else None,
        "most_active_reader": {
            "reader_id": top_reader_row[0],
            "full_name": top_reader_row[1],
            "times": top_reader_row[2],
        } if top_reader_row else None,
    }



@router.get("/", response_model=list[ReportResponse])
def get_reports(
    librarian: Librarian = Depends(get_current_librarian),
    db: Session = Depends(get_db)
):

    repo = ReportRepository(db)

    return repo.get_all()



@router.get("/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: str,
    librarian: Librarian = Depends(get_current_librarian),
    db: Session = Depends(get_db)
):

    repo = ReportRepository(db)

    report = repo.get_by_id(report_id)


    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )


    return report
