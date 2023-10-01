from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from src.db.db import Base
from src.schemas.notifications import NotificationSchema


class Notifications(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    header: Mapped[str] = mapped_column(nullable=False)
    message: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(ForeignKey("notification_types.type"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    sent_datetime: Mapped[datetime] = mapped_column(nullable=False)
