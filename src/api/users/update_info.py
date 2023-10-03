from starlette.requests import Request

from src.api.users.router import router
from fastapi import status

from src.schemas.base import ResponseModel
from src.schemas.users import UserResponseModel, UserInfoModel
from src.api.dependencies import UOWDep
from src.services.users import UsersService
from src.utils.create_response import create_response


@router.post(
    "/update/info/{user_id}",
    status_code=status.HTTP_200_OK,
    description=(
            "Обновляет имя, логин или почту пользователя\n\n"
            "Update name, login or email of user"
    ),
    summary="update user info",
    response_model=UserResponseModel,
    responses={
        status.HTTP_200_OK: {
            "model": UserResponseModel,
            "description": "User info updated",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ResponseModel,
            "description": "User not authorized. Check message",
        },
        status.HTTP_409_CONFLICT: {
            "model": ResponseModel,
            "description": "User can edit only yourself",
        }
    }
)
async def update_user_info_handler(
        user_id: int,
        user_info: UserInfoModel,
        uow: UOWDep,
        request: Request
):
    sender_user_id = int(request.cookies.get("user_id", 0))
    user, err = await UsersService().get_user(uow, user_info={"id": user_id})
    if err:
        return create_response(
            content=ResponseModel(message=err),
            status=status.HTTP_409_CONFLICT
        )
    else:
        if user_id != sender_user_id:
            return create_response(
                content=ResponseModel(message="User can edit only yourself"),
                status=status.HTTP_409_CONFLICT
            )
        else:
            user, err = await UsersService().update_user_info(uow, user_id=sender_user_id, user_info=user_info.model_dump(exclude_none=True))
            if err:
                return create_response(
                    content=ResponseModel(message=err),
                    status=status.HTTP_409_CONFLICT
                )
            else:
                return create_response(
                    content=UserResponseModel(
                        data=user.to_read_model().model_dump(exclude=["id", "password"])
                    ),
                    status=status.HTTP_200_OK
                )
