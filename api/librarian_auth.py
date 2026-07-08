from fastapi import Depends, Header, HTTPException
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

    if not token:
        raise HTTPException(status_code=401, detail="Librarian authentication required")

    librarian = LibrarianRepository(db).get_by_id(token)
    if not librarian:
        raise HTTPException(status_code=403, detail="Only librarian can access this API")

    return librarian
