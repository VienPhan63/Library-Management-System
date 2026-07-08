from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.dependencies import get_db

from models import Report

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

        librarian_id=request.librarian_id

    )


    report_repo.create(report)

    db.commit()

    db.refresh(report)


    return report



@router.get("/", response_model=list[ReportResponse])
def get_reports(
    db: Session = Depends(get_db)
):

    repo = ReportRepository(db)

    return repo.get_all()



@router.get("/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: str,
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