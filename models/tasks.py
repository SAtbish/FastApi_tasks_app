from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from db.db import Base


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
