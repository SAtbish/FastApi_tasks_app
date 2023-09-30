from src.api.users.router import router
from fastapi.responses import JSONResponse
from fastapi import status

from src.schemas.base import ResponseModel
from src.schemas.users import UserDeletionInfo
from src.api.dependencies import UOWDep, AuthorizationDep
from src.services.users import UsersService


@router.post(
    "/delete/{user_id}",
    status_code=status.HTTP_200_OK,
    description=(
            "Удаляет пользователя по id\n\n"
            "Delete user by id"
    ),
    summary="delete user",
    response_model=UserDeletionInfo,
    responses={
        status.HTTP_200_OK: {
            "model": UserDeletionInfo,
            "description": "User deleted",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ResponseModel,
            "description": "User not authorized. Check message",
        },
        status.HTTP_409_CONFLICT: {
            "model": ResponseModel,
            "description": "User can delete only yourself",
        }
    }
)
async def delete_user_handler(
        user_id: int,
        tokens: AuthorizationDep,
        uow: UOWDep
):
    if tokens["user_id"] == user_id:
        deletion_info = await UsersService().delete_user_by_id(uow, user_id=user_id)
        response = JSONResponse(
            content=UserDeletionInfo(**deletion_info).model_dump(),
            status_code=status.HTTP_200_OK
        )
    else:
        response = JSONResponse(
            content=ResponseModel(message="User can delete only yourself").model_dump(),
            status_code=status.HTTP_409_CONFLICT
        )
    for key, value in tokens.items():
        response.set_cookie(key, value)

    return response
