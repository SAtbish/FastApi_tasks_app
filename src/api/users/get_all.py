from src.api.users.router import router
from fastapi.responses import JSONResponse
from fastapi import status

from src.schemas.base import ResponseModel
from src.schemas.users import UsersResponseModel
from src.api.dependencies import UOWDep
from src.services.users import UsersService
from fastapi_cache.decorator import cache


@router.get(
    "/get/all",
    status_code=status.HTTP_200_OK,
    description=(
            "Получает всех пользователей\n\n"
            "Get all users"
    ),
    summary="getting users",
    response_model=UsersResponseModel,
    responses={
        status.HTTP_200_OK: {
            "model": UsersResponseModel,
            "description": "Got users",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ResponseModel,
            "description": "User not authorized. Check message",
        }
    }
)
@cache(expire=60)
async def get_all_users_handler(
        uow: UOWDep
):
    users = await UsersService().get_all(uow)
    response = JSONResponse(
        content=UsersResponseModel(data=[user.model_dump(exclude=["id", "password"]) for user in users]).model_dump(),
        status_code=status.HTTP_200_OK
    )

    return response
