from src.api.users.router import router
from fastapi.responses import JSONResponse
from fastapi import status

from src.schemas.base import ResponseModel
from src.schemas.users import UserResponseModel, GetUserRequest
from src.api.dependencies import UOWDep, AuthorizationDep
from src.services.users import UsersService


@router.post(
    "/get",
    status_code=status.HTTP_200_OK,
    description=(
            "Получает пользователя по определённым полям\n\n"
            "Get user by fields"
    ),
    summary="get user",
    response_model=UserResponseModel,
    responses={
        status.HTTP_200_OK: {
            "model": UserResponseModel,
            "description": "Got user",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ResponseModel,
            "description": "User not authorized. Check message",
        },
        status.HTTP_409_CONFLICT: {
            "model": ResponseModel,
            "description": "Can not find user. Check message",
        }
    }
)
async def get_user_handler(
        user_info: GetUserRequest,
        tokens: AuthorizationDep,
        uow: UOWDep
):
    user_info = user_info.model_dump(exclude_none=True)
    user, err = await UsersService().get_user(uow, user_info)
    if err:
        response = JSONResponse(
            content=ResponseModel(message=err).__dict__,
            status_code=status.HTTP_409_CONFLICT
        )
    else:
        response = JSONResponse(
            content=UserResponseModel(data=user.model_dump(exclude=["id", "password"])).model_dump(),
            status_code=status.HTTP_200_OK
        )
    for key, value in tokens.items():
        response.set_cookie(key, value)

    return response
