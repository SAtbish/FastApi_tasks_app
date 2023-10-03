from src.api.users.router import router
from fastapi import status

from src.schemas.base import ResponseModel
from src.schemas.users import UserResponseModel, GetUserRequest
from src.api.dependencies import UOWDep
from src.services.users import UsersService
from src.utils.create_response import create_response


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
        uow: UOWDep
):
    user_info = user_info.model_dump(exclude_none=True)
    user, err = await UsersService().get_user(uow, user_info)
    if err:
        return create_response(
            content=ResponseModel(message=err),
            status=status.HTTP_409_CONFLICT
        )
    else:
        return create_response(
            content=UserResponseModel(data=user.model_dump(exclude=["id", "password"])),
            status=status.HTTP_200_OK
        )
