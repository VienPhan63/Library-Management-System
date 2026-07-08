from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session

from database.dependencies import get_db
from models import Book, Librarian
from models.book import BookStatus
from repositories import BookRepository, LibrarianRepository
from schemas.book import BookCreate, BookResponse, BookUpdate


router = APIRouter(prefix="/books", tags=["Books"])


def _get_or_create_default_librarian(db: Session) -> Librarian:
    repo = LibrarianRepository(db)
    librarian = next(iter(repo.get_all()), None)

    if librarian:
        return librarian

    librarian = repo.create(
        Librarian(
            full_name="Default Librarian",
            phone_number="0000000000",
            email="default.librarian@library.local",
            password="default-password",
        )
    )
    db.flush()
    return librarian


def _get_librarian_id(
    db: Session,
    librarian_id: str | None = None,
    fallback_librarian: Librarian | None = None,
) -> str:
    if librarian_id:
        librarian_repo = LibrarianRepository(db)
        if not librarian_repo.exists(librarian_id):
            raise HTTPException(status_code=404, detail="Librarian not found")
        return librarian_id

    if fallback_librarian:
        return fallback_librarian.id

    return _get_or_create_default_librarian(db).id


def _get_optional_librarian(
    authorization: str | None = Header(default=None),
    x_librarian_id: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> Librarian | None:
    token = x_librarian_id

    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()

    if not token:
        return None

    return LibrarianRepository(db).get_by_id(token)


def _get_payload_data(payload: BookCreate | BookUpdate) -> dict[str, Any]:
    if hasattr(payload, "model_dump"):
        return payload.model_dump(exclude_unset=True)
    return payload.dict(exclude_unset=True)


def _validate_inventory(quantity: int, available_quantity: int) -> None:
    if available_quantity > quantity:
        raise HTTPException(
            status_code=400,
            detail="Available quantity cannot exceed quantity",
        )


def _resolve_status(data: dict[str, Any], available_quantity: int) -> BookStatus:
    if "status" in data and data["status"] is not None:
        status_value = data["status"]
        if isinstance(status_value, str):
            return BookStatus(status_value)
        return status_value

    return BookStatus.AVAILABLE if available_quantity > 0 else BookStatus.UNAVAILABLE


@router.get("", response_model=list[BookResponse])
@router.get("/", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db)):
    repo = BookRepository(db)
    return repo.get_all()


@router.get("/search", response_model=list[BookResponse])
@router.get("/search/", response_model=list[BookResponse])
def search_books(
    keyword: str = Query(default=""),
    category: str | None = None,
    status: BookStatus | None = None,
    db: Session = Depends(get_db),
):
    repo = BookRepository(db)
    books = repo.search(keyword) if keyword else repo.get_all()

    if category:
        books = [book for book in books if book.category.lower() == category.lower()]

    if status:
        books = [book for book in books if book.status == status]

    return books


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: str, db: Session = Depends(get_db)):
    repo = BookRepository(db)
    book = repo.get_by_id(book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@router.post("", response_model=BookResponse, status_code=201)
@router.post("/", response_model=BookResponse, status_code=201)
def create_book(
    payload: BookCreate,
    librarian: Librarian | None = Depends(_get_optional_librarian),
    db: Session = Depends(get_db),
):
    repo = BookRepository(db)
    available_quantity = payload.available_quantity
    if available_quantity is None:
        available_quantity = payload.quantity

    _validate_inventory(payload.quantity, available_quantity)

    data = _get_payload_data(payload)
    status = _resolve_status(data, available_quantity)

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
        librarian_id=_get_librarian_id(
            db,
            payload.librarian_id,
            fallback_librarian=librarian,
        ),
    )

    repo.create(book)
    db.commit()
    db.refresh(book)
    return book


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: str,
    payload: BookUpdate,
    librarian: Librarian | None = Depends(_get_optional_librarian),
    db: Session = Depends(get_db),
):
    repo = BookRepository(db)
    book = repo.get_by_id(book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    data = _get_payload_data(payload)
    if "librarian_id" in data:
        data["librarian_id"] = _get_librarian_id(
            db,
            data["librarian_id"],
            fallback_librarian=librarian,
        )

    if "quantity" in data:
        quantity = data["quantity"]
    else:
        quantity = book.quantity

    available_quantity = data.get("available_quantity", book.available_quantity)
    if available_quantity is None:
        available_quantity = quantity

    _validate_inventory(quantity, available_quantity)

    for field, value in data.items():
        setattr(book, field, value)

    if "available_quantity" in data:
        book.available_quantity = available_quantity

    if "quantity" in data:
        book.quantity = quantity

    book.status = _resolve_status(data, available_quantity)

    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}")
def delete_book(
    book_id: str,
    librarian: Librarian | None = Depends(_get_optional_librarian),
    db: Session = Depends(get_db),
):
    repo = BookRepository(db)
    book = repo.get_by_id(book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    repo.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}