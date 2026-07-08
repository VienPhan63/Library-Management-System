from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.librarian_auth import get_current_librarian
from database.dependencies import get_db
from models import Librarian, LibraryCard, LibraryCardStatus, Reader
from models.reader import ReaderStatus


router = APIRouter(prefix="/readers", tags=["Readers"])


def _reader_response(reader: Reader, card: LibraryCard | None = None) -> dict:
    return {
        "id": reader.id,
        "full_name": reader.full_name,
        "email": reader.email,
        "phone_number": reader.phone_number,
        "gender": reader.gender,
        "date_of_birth": reader.date_of_birth,
        "status": reader.status,
        "card_code": card.card_code if card else reader.id,
        "card_status": card.status if card else reader.status,
    }


@router.get("")
@router.get("/")
def get_readers(
    keyword: str = Query(default=""),
    librarian: Librarian = Depends(get_current_librarian),
    db: Session = Depends(get_db),
):
    stmt = select(Reader)
    if keyword.strip():
        value = f"%{keyword.strip()}%"
        stmt = stmt.where(
            (Reader.full_name.ilike(value))
            | (Reader.email.ilike(value))
            | (Reader.id.ilike(value))
        )

    readers = list(db.scalars(stmt))
    cards = {}
    if readers:
        cards = {
            card.reader_id: card
            for card in db.scalars(
                select(LibraryCard).where(
                    LibraryCard.reader_id.in_([reader.id for reader in readers])
                )
            )
        }
    return [_reader_response(reader, cards.get(reader.id)) for reader in readers]


@router.get("/{reader_id}")
def get_reader(
    reader_id: str,
    librarian: Librarian = Depends(get_current_librarian),
    db: Session = Depends(get_db),
):
    card = db.scalar(select(LibraryCard).where(LibraryCard.card_code == reader_id))
    reader = card.reader if card else db.get(Reader, reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")

    if not card:
        card = db.scalar(select(LibraryCard).where(LibraryCard.reader_id == reader.id))
    return _reader_response(reader, card)


@router.patch("/{reader_id}/block")
def block_reader(
    reader_id: str,
    librarian: Librarian = Depends(get_current_librarian),
    db: Session = Depends(get_db),
):
    card = db.scalar(select(LibraryCard).where(LibraryCard.card_code == reader_id))
    reader = card.reader if card else db.get(Reader, reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")

    reader.status = ReaderStatus.BLOCKED
    if card:
        card.status = LibraryCardStatus.BLOCKED
    db.commit()
    return {"message": "Reader card blocked successfully"}


@router.patch("/{reader_id}/unblock")
def unblock_reader(
    reader_id: str,
    librarian: Librarian = Depends(get_current_librarian),
    db: Session = Depends(get_db),
):
    card = db.scalar(select(LibraryCard).where(LibraryCard.card_code == reader_id))
    reader = card.reader if card else db.get(Reader, reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")

    reader.status = ReaderStatus.ACTIVE
    if card:
        card.status = LibraryCardStatus.ACTIVE
    db.commit()
    return {"message": "Reader card unblocked successfully"}
