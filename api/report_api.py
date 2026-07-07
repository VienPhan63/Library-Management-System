from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.dependencies import get_db
from repositories import BookRepository, BorrowRecordRepository
from repositories.report_repository import ReportRepository


router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.get("/summary")
def get_report_summary(db: Session = Depends(get_db)):
    book_repo = BookRepository(db)
    borrow_repo = BorrowRecordRepository(db)
    report_repo = ReportRepository(db)

    books = book_repo.get_all()

    return {
        "total_titles": len(books),
        "total_categories": len({book.category for book in books}),
        "total_stock": sum(book.quantity for book in books),
        "currently_borrowed": borrow_repo.count_borrowing(),
        "total_returns": borrow_repo.count_returned(),
        "total_borrows": borrow_repo.count(),
        "total_fines": report_repo.get_total_fine(
            start_date=date.min,
            end_date=date.max,
        ),
    }
