from sqlalchemy.orm import mapped_column
from sqlalchemy import func, DateTime

class TimestampMixin:

    created_at = mapped_column(
        DateTime,
        server_default=func.now()
    )

    updated_at = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )