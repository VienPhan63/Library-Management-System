from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from api.librarian_auth import get_current_librarian
from database.dependencies import get_db
from models import Book, Librarian
from models.book import BookStatus
from repositories import BookRepository, LibrarianRepository
from schemas.book import BookCreate, BookResponse, BookUpdate


router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


def _get_librarian_id(db: Session, librarian_id: str | None) -> str:
    librarian_repo = LibrarianRepository(db)

    if librarian_id:
        if not librarian_repo.exists(librarian_id):
            raise HTTPException(status_code=404, detail="Librarian not found")
        return librarian_id

    librarian = next(iter(librarian_repo.get_all()), None)
    if not librarian:
        librarian = librarian_repo.create(
            Librarian(
                full_name="Default Librarian",
                phone_number="0000000000",
                email="default.librarian@library.local",
                password="default-password",
            )
        )
        db.flush()

    return librarian.id


@router.get("/", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db)):
    repo = BookRepository(db)
    return repo.get_all()


@router.get("/search/", response_model=list[BookResponse])
@router.get("/search", response_model=list[BookResponse])
def search_books(
    keyword: str = Query(default=""),
    category: str | None = None,
    status: BookStatus | None = None,
    db: Session = Depends(get_db)
):
    repo = BookRepository(db)
    books = repo.search(keyword) if keyword else repo.get_all()

    if category:
        books = [
            book for book in books
            if book.category.lower() == category.lower()
        ]

    if status:
        books = [
            book for book in books
            if book.status == status
        ]

    return books


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: str, db: Session = Depends(get_db)):
    repo = BookRepository(db)
    book = repo.get_by_id(book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@router.post("/", response_model=BookResponse, status_code=201)
def create_book(
    payload: BookCreate,
    librarian: Librarian = Depends(get_current_librarian),
    db: Session = Depends(get_db)
):
    repo = BookRepository(db)
    available_quantity = (
        payload.quantity
        if payload.available_quantity is None
        else payload.available_quantity
    )

    if available_quantity > payload.quantity:
        raise HTTPException(
            status_code=400,
            detail="Available quantity cannot exceed quantity"
        )

    status = BookStatus.AVAILABLE if available_quantity > 0 else BookStatus.UNAVAILABLE

    book = Book(
        title=payload.title,
        author=payload.author,
        publisher=payload.publisher,
        publish_year=payload.publish_year,
        category=payload.category,
        description=payload.description,
        quantity=payload.quantity,
        price=payload.price,
        available_quantity=available_quantity,
        status=status,
        librarian_id=_get_librarian_id(db, payload.librarian_id or librarian.id),
    )

    repo.create(book)
    db.commit()
    db.refresh(book)

    return book


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: str,
    payload: BookUpdate,
    librarian: Librarian = Depends(get_current_librarian),
    db: Session = Depends(get_db)
):
    repo = BookRepository(db)
    book = repo.get_by_id(book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    data = payload.dict(exclude_unset=True)
    if "librarian_id" in data:
        data["librarian_id"] = _get_librarian_id(db, data["librarian_id"])

    for field, value in data.items():
        setattr(book, field, value)

    if book.available_quantity > book.quantity:
        raise HTTPException(
            status_code=400,
            detail="Available quantity cannot exceed quantity"
        )

    book.status = BookStatus.AVAILABLE if book.available_quantity > 0 else BookStatus.UNAVAILABLE

    db.commit()
    db.refresh(book)

    return book


@router.delete("/{book_id}")
def delete_book(
    book_id: str,
    librarian: Librarian = Depends(get_current_librarian),
    db: Session = Depends(get_db)
):
    repo = BookRepository(db)
    book = repo.get_by_id(book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    repo.delete(book)
    db.commit()

    return {"message": "Book deleted successfully"}