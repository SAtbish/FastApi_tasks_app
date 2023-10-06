from datetime import datetime
from typing import Any

from src.enums import Error
from src.utils.unitofwork import IUnitOfWork
from secrets import token_urlsafe


class TokensService:
    @staticmethod
    async def create_token(uow: IUnitOfWork, user_id: int):
        async with uow:
            new_token = await uow.tokens.create_one(
                data={
                    "access_token": token_urlsafe(64),
                    "refresh_token": token_urlsafe(64),
                    "data_time": datetime.now(),
                    "user_id": user_id
                }
            )
            await uow.commit()
            return new_token.model_dump(exclude=["id"])

    @staticmethod
    async def get_token(uow: IUnitOfWork, access_token: int):
        async with uow:
            token = await uow.tokens.read_one(access_token=access_token)
            if not token:
                return {}, "token_not_exist"
            else:
                return token.to_read_model(), None

    @staticmethod
    async def renew_token(uow: IUnitOfWork, user_id: int, refresh_token: str) -> tuple[dict[str | Any], Error]:
        async with uow:
            token_data, err = await uow.tokens.renew_token(user_id=user_id, refresh_token=refresh_token)
            if err:
                return {}, err
            await uow.commit()
            return token_data, None
