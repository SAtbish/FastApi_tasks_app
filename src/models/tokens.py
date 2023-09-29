from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from src.db.db import Base
from src.schemas.tokens import TokensSchema


class Tokens(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    access_token: Mapped[str] = mapped_column(nullable=False)
    refresh_token: Mapped[str] = mapped_column(nullable=False)
    data_time: Mapped[datetime] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    is_permanent: Mapped[bool] = mapped_column(default=False)

    def to_read_model(self) -> TokensSchema:
        return TokensSchema(
            id=self.id,
            access_token=self.access_token,
            refresh_token=self.refresh_token,
            data_time=self.data_time,
            user_id=self.user_id,
            is_permanent=self.is_permanent
        )
