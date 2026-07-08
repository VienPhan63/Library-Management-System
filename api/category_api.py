from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.librarian_auth import get_current_librarian
from database.dependencies import get_db
from models import Category, Librarian
from schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate


router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.get("/", response_model=list[CategoryResponse])
@router.get("", response_model=list[CategoryResponse])
def get_categories(
    keyword: str = Query(default=""),
    db: Session = Depends(get_db),
):
    stmt = select(Category)
    if keyword.strip():
        stmt = stmt.where(Category.name.ilike(f"%{keyword.strip()}%"))
    return list(db.scalars(stmt))


@router.post("/", response_model=CategoryResponse, status_code=201)
@router.post("", response_model=CategoryResponse, status_code=201)
def create_category(
    payload: CategoryCreate,
    librarian: Librarian = Depends(get_current_librarian),
    db: Session = Depends(get_db),
):
    exists = db.scalar(select(Category).where(Category.name == payload.name))
    if exists:
        raise HTTPException(status_code=400, detail="Category already exists")

    category = Category(
        name=payload.name,
        description=payload.description,
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: str,
    payload: CategoryUpdate,
    librarian: Librarian = Depends(get_current_librarian),
    db: Session = Depends(get_db),
):
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}")
def delete_category(
    category_id: str,
    librarian: Librarian = Depends(get_current_librarian),
    db: Session = Depends(get_db),
):
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}
