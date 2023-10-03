from src.api.users.router import router
from fastapi import status

from src.schemas.base import ResponseModel
from src.schemas.users import UserRegistration, UserResponseModel, UserInfo
from src.api.dependencies import UOWDep
from src.services.users import UsersService
from src.utils.create_response import create_response


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
        return create_response(
            content=ResponseModel(message=err),
            status=status.HTTP_409_CONFLICT
        )
    return create_response(
        content=UserResponseModel(
            message="User registered",
            data=UserInfo(**user_data)
        ),
        status=status.HTTP_201_CREATED
    )
