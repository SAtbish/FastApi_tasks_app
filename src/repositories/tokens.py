from datetime import datetime, timedelta
from typing import Any

from config import TOKEN_UPDATE_TIME
from src.enums import Error
from src.models.tokens import Tokens
from src.schemas.tokens import TokensSchema
from src.utils.repository import SQLAlchemyRepository
from secrets import token_urlsafe


class TokensRepository(SQLAlchemyRepository):
    model = Tokens

    async def get_user_token(self, user_id: int) -> TokensSchema:
        token = await self.read_one(user_id=user_id)
        if not token:
            return await self.create_one(
                data={
                    "access_token": token_urlsafe(64),
                    "refresh_token": token_urlsafe(64),
                    "data_time": datetime.now(),
                    "user_id": user_id
                }
            )
        else:
            return token.to_read_model()

    async def renew_token(self, user_id: int, refresh_token: str) -> tuple[dict[str | Any], Error]:
        token = await self.read_one(user_id=user_id)
        if not token:
            return {}, "token_not_exist"

        diff: timedelta = datetime.now() - token.data_time
        diff_seconds = int(diff.total_seconds())

        if diff_seconds <= TOKEN_UPDATE_TIME or token.is_permanent:
            return {
                "access_token": token.access_token,
                "user_id": user_id,
                "refresh_token": token.refresh_token,
            }, None
        else:
            if refresh_token == token.refresh_token:
                new_token_data = {
                    "access_token": token_urlsafe(64),
                    "refresh_token": token_urlsafe(64),
                    "data_time": datetime.now(),
                }
                await self.update_one(obj_id=token.id, data=new_token_data)
                new_token_data["user_id"] = user_id
                del new_token_data["data_time"]
                return new_token_data, None
