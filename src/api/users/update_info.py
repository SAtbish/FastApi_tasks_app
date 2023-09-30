from src.api.users.router import router
from fastapi.responses import JSONResponse
from fastapi import status

from src.schemas.base import ResponseModel
from src.schemas.users import UserResponseModel, UserInfoModel
from src.api.dependencies import UOWDep, AuthorizationDep
from src.services.users import UsersService


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
        tokens: AuthorizationDep,
        uow: UOWDep
):
    user_info = user_info.model_dump(exclude_none=True)
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
            user, err = await UsersService().update_user_info(uow, user_id=tokens["user_id"], user_info=user_info)
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
