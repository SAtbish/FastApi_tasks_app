from sqlalchemy.orm import Mapped, mapped_column
from src.db.db import Base
from src.schemas.users import UserSchema


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    login: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    is_confirmed: Mapped[bool] = mapped_column(default=False)

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            name=self.name,
            login=self.login,
            email=self.email,
            password=self.password,
            is_confirmed=self.is_confirmed
        )
