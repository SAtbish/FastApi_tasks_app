from src.api.users.router import router
from fastapi.responses import JSONResponse
from fastapi import status

from src.schemas.base import ResponseModel
from src.schemas.users import UserResponseModel, ChangeUserPassword
from src.api.dependencies import UOWDep, AuthorizationDep
from src.services.users import UsersService


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
        tokens: AuthorizationDep,
        uow: UOWDep
):
    user, err = await UsersService().get_user(uow, user_info={"id": user_id})
    if err:
        response = JSONResponse(
            content=ResponseModel(message=err).__dict__,
            status_code=status.HTTP_409_CONFLICT
        )
    else:
        if user_id != tokens["user_id"]:
            response = JSONResponse(
                content=ResponseModel(message="User can edit only yourself").__dict__,
                status_code=status.HTTP_409_CONFLICT
            )
        else:
            user, err = await UsersService().update_user_password(
                uow,
                user_id=tokens["user_id"],
                old_password=passwords.old_password,
                new_password=passwords.new_password
            )
            if err:
                response = JSONResponse(
                    content=ResponseModel(message=err).__dict__,
                    status_code=status.HTTP_409_CONFLICT
                )
            else:
                response = JSONResponse(
                    content=UserResponseModel(
                        data=user.to_read_model().model_dump(exclude=["id", "password"])
                    ).model_dump(),
                    status_code=status.HTTP_200_OK
                )

    for key, value in tokens.items():
        response.set_cookie(key, value)

    return response
