from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from src.db.db import Base
from src.schemas.tasks import TasksSchema


class Tasks(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    assignee_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    creation_date: Mapped[datetime] = mapped_column(nullable=False)
    expiration_date: Mapped[datetime]
    is_done: Mapped[bool] = mapped_column(default=False)
    done_date: Mapped[datetime]

    def to_read_model(self) -> TasksSchema:
        return TasksSchema(
            id=self.id,
            title=self.title,
            author_id=self.author_id,
            assignee_id=self.assignee_id,
            creation_date=self.creation_date,
            expiration_date=self.expiration_date,
            is_done=self.is_done,
            done_date=self.done_date
        )
