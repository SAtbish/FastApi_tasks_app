import json
from typing import Callable, Any

from fastapi import Request, status, HTTPException
from src.utils.unitofwork import UnitOfWork
from src.services.tokens import TokensService


def user_authorization_wrapper() -> Callable[[Request], Any]:
    async def user_authorization(request: Request):
        try:
            json_request = await request.json()
        except json.JSONDecodeError:
            json_request = {}

        args_request = dict(request.query_params)

        user_tokens = {
            "access_token": request.cookies.get("access_token"),
            "refresh_token": request.cookies.get("refresh_token", ""),
        }

        if not user_tokens.get("access_token"):
            user_tokens = {
                "access_token": json_request.get("access_token"),
                "refresh_token": json_request.get("refresh_token"),
            }

            if not user_tokens.get("access_token"):
                user_tokens["access_token"] = args_request.get("access_token")
                user_tokens["refresh_token"] = args_request.get("refresh_token")

            if not user_tokens.get("access_token"):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Failed to get access_token",
                )

        user_tokens.setdefault("refresh_token", "")

        uow = UnitOfWork()
        token, err = await TokensService().get_token(uow=uow, access_token=user_tokens["access_token"])
        if err:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=err,
            )

        updated_token, err = await TokensService().renew_token(
            uow=uow,
            user_id=token.user_id,
            refresh_token=token.refresh_token
        )
        if err:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=err,
            )

        return updated_token

    return user_authorization
