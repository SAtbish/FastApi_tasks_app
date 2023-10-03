from fastapi import Request
from src.utils.unitofwork import UnitOfWork
from src.services.tokens import TokensService


async def user_authorization(request: Request):

    args_request = dict(request.query_params)

    user_tokens = {
        "access_token": request.cookies.get("access_token"),
        "refresh_token": request.cookies.get("refresh_token", ""),
    }

    if not user_tokens.get("access_token"):
        user_tokens["access_token"] = args_request.get("access_token")
        user_tokens["refresh_token"] = args_request.get("refresh_token")

        if not user_tokens.get("access_token"):
            return {}, "Failed to get access_token"

    user_tokens.setdefault("refresh_token", "")

    uow = UnitOfWork()
    token, err = await TokensService().get_token(uow=uow, access_token=user_tokens["access_token"])
    if err:
        return {}, err

    updated_token, err = await TokensService().renew_token(
        uow=uow,
        user_id=token.user_id,
        refresh_token=token.refresh_token
    )
    if err:
        return {}, err

    return updated_token, None
