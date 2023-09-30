from src.api.users.router import router
from fastapi.responses import JSONResponse
from fastapi import status

from src.schemas.base import ResponseModel
from src.schemas.users import UserRegistration, UserResponseModel, UserInfo
from src.api.dependencies import UOWDep
from src.services.users import UsersService


@router.post(
    "/registration",
    response_model=UserResponseModel | ResponseModel,
    status_code=status.HTTP_200_OK,
    description=(
            "Регистрирует пользователя\n\n"
            "Registrate user"
    ),
    summary="Create user",
    responses={
        status.HTTP_201_CREATED: {
            "model": UserResponseModel,
            "description": "User created",
        },
        status.HTTP_409_CONFLICT: {
            "model": ResponseModel,
            "description": "User not created. Check message",
        }
    }
)
async def user_registration_handler(
        user: UserRegistration,
        uow: UOWDep,
):
    user_data, err = await UsersService().create_user(uow, user)
    if err:
        return JSONResponse(
            content=ResponseModel(message=err).__dict__,
            status_code=status.HTTP_409_CONFLICT
        )
    return JSONResponse(
        content=UserResponseModel(
            message="User registered",
            data=UserInfo(**user_data)
        ).model_dump(),
        status_code=status.HTTP_201_CREATED
    )
