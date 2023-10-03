from starlette.requests import Request

from src.api.users.router import router
from fastapi import status

from src.schemas.base import ResponseModel
from src.schemas.users import UserResponseModel, ChangeUserPassword
from src.api.dependencies import UOWDep
from src.services.users import UsersService
from src.utils.create_response import create_response


@router.post(
    "/update/password/{user_id}",
    status_code=status.HTTP_200_OK,
    description=(
            "Обновляет пароль пользователя\n\n"
            "Update password of user"
    ),
    summary="update user password",
    response_model=UserResponseModel,
    responses={
        status.HTTP_200_OK: {
            "model": UserResponseModel,
            "description": "User password updated",
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
async def update_user_password_handler(
        user_id: int,
        passwords: ChangeUserPassword,
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
            user, err = await UsersService().update_user_password(
                uow,
                user_id=sender_user_id,
                old_password=passwords.old_password,
                new_password=passwords.new_password
            )
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
