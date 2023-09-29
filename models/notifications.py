from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from db.db import Base


class Notifications(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    header: Mapped[str] = mapped_column(nullable=False)
    message: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[int] = mapped_column(ForeignKey("notification_types.type"), nullable=False)
    recipient: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    sent_datetime: Mapped[datetime] = mapped_column(nullable=False)
    is_read: Mapped[bool] = mapped_column(default=False)
    read_datetime: Mapped[datetime]
