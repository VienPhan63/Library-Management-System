from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    description: str | None = None


class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = None


class CategoryResponse(BaseModel):
    id: str
    name: str
    description: str | None = None

    model_config = {
        "from_attributes": True
    }
