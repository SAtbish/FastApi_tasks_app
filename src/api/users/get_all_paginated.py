from src.api.users.router import router
from fastapi import status
from fastapi_pagination import Page

from src.schemas.users import UserSchema
from src.api.dependencies import UOWDep
from src.services.users import UsersService
from fastapi_cache.decorator import cache


@router.get(
    "/get/all/paginated",
    status_code=status.HTTP_200_OK,
    description=(
            "Получает всех пользователей с пагинацией\n\n"
            "Get all users paginated"
    ),
    summary="getting users paginated",
    response_model=Page[UserSchema]
)
@cache(expire=60)
async def get_all_users_paginated_handler(
        uow: UOWDep
):
    users = await UsersService().get_all_paginated(uow)
    return users
