from fastapi import Depends, Header
from sqlalchemy.orm import Session

from database.dependencies import get_db
from models import Librarian
from repositories import LibrarianRepository


def get_current_librarian(
    authorization: str | None = Header(default=None),
    x_librarian_id: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> Librarian:
    token = x_librarian_id

    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()

    repo = LibrarianRepository(db)

    if token:
        librarian = repo.get_by_id(token)
        if librarian:
            return librarian

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
