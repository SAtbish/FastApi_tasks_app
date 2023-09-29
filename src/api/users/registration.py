from src.api.users.router import router
from fastapi.responses import JSONResponse
from fastapi import status

from src.schemas.base import ResponseModel
from src.schemas.users import UserRegistration
from src.api.dependencies import UOWDep
from src.services.users import UsersService


@router.post(
    "/registration",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    description=(
            "Регистрирует пользователя\n\n"
            "Registrate user"
    ),
    summary="Create user",
    responses={
        status.HTTP_201_CREATED: {
            "model": ResponseModel,
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
    user_id, err = await UsersService().create_user(uow, user)
    if err:
        return JSONResponse(
            content=ResponseModel(message=err).__dict__,
            status_code=status.HTTP_409_CONFLICT
        )
    return JSONResponse(
        content=ResponseModel(
            message="User registered",
            data={
                "user_id": user_id
            }
        ).__dict__,
        status_code=status.HTTP_201_CREATED
    )
