from src.api.users.router import router
from fastapi import status

from src.schemas.base import ResponseModel
from src.api.dependencies import UOWDep
from src.services.users import UsersService

from src.utils.create_response import create_response


@router.get(
    "/confirm/email/{user_id}/{email_hash}",
    status_code=status.HTTP_200_OK,
    description=(
            "Подтверждает почту пользователя\n\n"
            "Confirm user email"
    ),
    summary="confirm email",
    response_model=ResponseModel,
    responses={
        status.HTTP_200_OK: {
            "model": ResponseModel,
            "description": "Email confirmed",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ResponseModel,
            "description": "Email not confirmed. Check message",
        }
    }
)
async def confirm_user_email_handler(
        user_id: int,
        email_hash: str,
        uow: UOWDep
):
    err = await UsersService().confirm_user_email(uow=uow, email_hash=email_hash, user_info={"id": user_id})
    if err:
        return create_response(
            content=ResponseModel(message=err),
            status=status.HTTP_409_CONFLICT
        )
    else:
        return create_response(
            content=ResponseModel(message="Email confirmed"),
            status=status.HTTP_200_OK
        )
