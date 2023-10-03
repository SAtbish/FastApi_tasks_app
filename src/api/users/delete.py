from starlette.requests import Request

from src.api.users.router import router
from fastapi import status

from src.schemas.base import ResponseModel
from src.schemas.users import UserDeletionResponse, UserDeletionInfo
from src.api.dependencies import UOWDep
from src.services.users import UsersService
from src.utils.create_response import create_response


@router.post(
    "/delete/{user_id}",
    status_code=status.HTTP_200_OK,
    description=(
            "Удаляет пользователя по id\n\n"
            "Delete user by id"
    ),
    summary="delete user",
    response_model=UserDeletionResponse,
    responses={
        status.HTTP_200_OK: {
            "model": UserDeletionResponse,
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
        uow: UOWDep,
        request: Request
):
    sender_user_id = int(request.cookies.get("user_id", 0))
    if sender_user_id == user_id:
        deletion_info = await UsersService().delete_user_by_id(uow, user_id=user_id)
        return create_response(
            content=UserDeletionResponse(
                data=UserDeletionInfo(**deletion_info)
            ),
            status=status.HTTP_200_OK
        )
    else:
        return create_response(
            content=ResponseModel(message="User can delete only yourself"),
            status=status.HTTP_409_CONFLICT
        )
