from pydantic import BaseModel, Field

from models.book import BookStatus


class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=30)
    publisher: str = Field(min_length=1, max_length=30)
    publish_year: int
    category: str = Field(min_length=1, max_length=30)
    description: str = Field(default="", max_length=100)
    quantity: int = Field(ge=0)
    price: int = Field(default=0, ge=0)
    available_quantity: int | None = Field(default=None, ge=0)
    status: BookStatus = BookStatus.AVAILABLE
    librarian_id: str | None = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    author: str | None = Field(default=None, min_length=1, max_length=30)
    publisher: str | None = Field(default=None, min_length=1, max_length=30)
    publish_year: int | None = None
    category: str | None = Field(default=None, min_length=1, max_length=30)
    description: str | None = Field(default=None, max_length=100)
    quantity: int | None = Field(default=None, ge=0)
    price: int | None = Field(default=None, ge=0)
    available_quantity: int | None = Field(default=None, ge=0)
    status: BookStatus | None = None
    librarian_id: str | None = None


class BookResponse(BaseModel):
    id: str
    title: str
    author: str
    publisher: str
    publish_year: int
    category: str
    description: str
    quantity: int
    price: int
    available_quantity: int
    status: BookStatus
    librarian_id: str

    model_config = {
        "from_attributes": True
    }
