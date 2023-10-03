from src.api.users.router import router
from fastapi import status

from src.schemas.base import ResponseModel
from src.schemas.users import UserLogin
from src.api.dependencies import UOWDep
from src.services.users import UsersService
from src.utils.create_response import create_response


@router.post(
    "/login",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    description=(
            "Авторизация пользователя\n\n"
            "User Authorization"
    ),
    summary="Authorize user",
    responses={
        status.HTTP_200_OK: {
            "model": ResponseModel,
            "description": "User authorized",
        },
        status.HTTP_409_CONFLICT: {
            "model": ResponseModel,
            "description": "User not authorized. Check message",
        }
    }
)
async def user_login_handler(
        user: UserLogin,
        uow: UOWDep,
):
    user_tokens, err = await UsersService().login_user(uow, user)
    if err:
        response = create_response(
            content=ResponseModel(message=err),
            status=status.HTTP_409_CONFLICT
        )
    else:
        response = create_response(
            content=ResponseModel(
                message="User log in"
            ),
            status=status.HTTP_200_OK
        )
        response.set_cookie("access_token", user_tokens["access_token"], samesite="none", secure=True)
        response.set_cookie("refresh_token", user_tokens["refresh_token"], samesite="none", secure=True)
        response.set_cookie("user_id", user_tokens["user_id"], samesite="none", secure=True)

    return response
