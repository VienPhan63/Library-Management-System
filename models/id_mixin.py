from uuid import uuid4
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class IdMixin:
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4())
    )