from sqlalchemy.orm import Mapped, mapped_column
from db.db import Base


class NotificationTypes(Base):
    __tablename__ = "notification_types"

    type: Mapped[str] = mapped_column(nullable=False, primary_key=True)
    description: Mapped[str] = mapped_column(nullable=False)
