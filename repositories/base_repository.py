from typing import Generic, Type, TypeVar

from sqlalchemy import func, select
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):

    def __init__(
        self,
        model: Type[ModelType],
        session: Session
    ):
        self.model = model
        self.session = session

    # CREATE

    def create(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        return obj

    # READ

    def get_by_id(self, object_id: str)  -> ModelType | None:

        stmt = (
            select(self.model)
            .where(self.model.id == object_id)
        )

        return self.session.scalar(stmt)

    def get_all(self):

        stmt = select(self.model)

        return list(self.session.scalars(stmt).all())

    def exists(self, object_id: str) -> bool:

        stmt = (
            select(func.count())
            .select_from(self.model)
            .where(self.model.id == object_id)
        )

        return bool(self.session.scalar(stmt))

    def count(self) -> int:

        stmt = (
            select(func.count())
            .select_from(self.model)
        )

        return self.session.scalar(stmt) or 0

    # UPDATE

    def update(self):

        self.session.flush()

    # DELETE

    def delete(self, obj: ModelType):

        self.session.delete(obj)

    # def commit(self):
    #     self.session.commit()


    # def rollback(self):
    #     self.session.rollback()