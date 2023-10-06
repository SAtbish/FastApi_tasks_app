from sqlalchemy.orm import Mapped, mapped_column
from src.db.db import Base
from src.schemas.notifications import NotificationTypesSchema


class NotificationTypes(Base):
    __tablename__ = "notification_types"

    type: Mapped[str] = mapped_column(nullable=False, primary_key=True)
    description: Mapped[str] = mapped_column(nullable=False)

    def to_read_model(self) -> NotificationTypesSchema:
        return NotificationTypesSchema(
            type=self.type,
            description=self.description
        )

