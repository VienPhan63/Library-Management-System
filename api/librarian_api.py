from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database.dependencies import get_db
from models import Librarian
from repositories import LibrarianRepository
from schemas.librarian import (
    LibrarianCreate,
    LibrarianResponse,
    LibrarianUpdate,
)

router = APIRouter(
    prefix="/librarians",
    tags=["Librarian"]
)


@router.post("/", response_model=LibrarianResponse)
def create_librarian(
    request: LibrarianCreate,
    db: Session = Depends(get_db)
):
    repo = LibrarianRepository(db)

    if repo.get_by_phone(request.phone_number):
        raise HTTPException(
            status_code=400,
            detail="Phone number already exists"
        )

    librarian = Librarian(
        full_name=request.full_name,
        phone_number=request.phone_number
    )

    repo.create(librarian)
    db.commit()
    db.refresh(librarian)

    return librarian


@router.get("/", response_model=list[LibrarianResponse])
def get_librarians(
    db: Session = Depends(get_db)
):
    repo = LibrarianRepository(db)
    return repo.get_all()


@router.get("/search", response_model=list[LibrarianResponse])
def search_librarians(
    keyword: str = Query(default=""),
    db: Session = Depends(get_db)
):
    repo = LibrarianRepository(db)

    if keyword.strip() == "":
        return repo.get_all()

    return repo.search(keyword)


@router.get("/{librarian_id}", response_model=LibrarianResponse)
def get_librarian_by_id(
    librarian_id: str,
    db: Session = Depends(get_db)
):
    repo = LibrarianRepository(db)
    librarian = repo.get_by_id(librarian_id)

    if librarian is None:
        raise HTTPException(
            status_code=404,
            detail="Librarian not found"
        )

    return librarian


@router.put("/{librarian_id}", response_model=LibrarianResponse)
def update_librarian(
    librarian_id: str,
    request: LibrarianUpdate,
    db: Session = Depends(get_db)
):
    repo = LibrarianRepository(db)
    librarian = repo.get_by_id(librarian_id)

    if librarian is None:
        raise HTTPException(
            status_code=404,
            detail="Librarian not found"
        )

    if request.phone_number and request.phone_number != librarian.phone_number:
        existing = repo.get_by_phone(request.phone_number)
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Phone number already exists"
            )
        librarian.phone_number = request.phone_number

    if request.full_name is not None:
        librarian.full_name = request.full_name

    repo.update()
    db.commit()
    db.refresh(librarian)

    return librarian


@router.delete("/{librarian_id}")
def delete_librarian(
    librarian_id: str,
    db: Session = Depends(get_db)
):
    repo = LibrarianRepository(db)
    librarian = repo.get_by_id(librarian_id)

    if librarian is None:
        raise HTTPException(
            status_code=404,
            detail="Librarian not found"
        )

    repo.delete(librarian)
    db.commit()

    return {
        "message": "Librarian deleted successfully"
    }
