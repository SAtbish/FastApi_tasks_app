from src.models.tokens import Tokens
from src.utils.repository import SQLAlchemyRepository


class TokensRepository(SQLAlchemyRepository):
    model = Tokens
