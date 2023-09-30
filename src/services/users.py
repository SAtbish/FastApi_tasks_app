from typing import Any

from src.enums import Error
from src.schemas.users import UserRegistration, UserLogin
from src.utils.unitofwork import IUnitOfWork
from werkzeug.security import generate_password_hash, check_password_hash


class UsersService:
    @staticmethod
    async def create_user(uow: IUnitOfWork, user: UserRegistration) -> tuple[dict[str | Any], Error]:
        async with uow:
            # checking for login existence
            exist_login = await uow.users.read_one(login=user.login)
            if exist_login:
                return {}, "login_exist"

            # checking for email existence
            exist_email = await uow.users.read_one(email=user.email)
            if exist_email:
                return {}, "email_exist"

            user.password = generate_password_hash(user.password)
            user_dict = user.model_dump()

            user_obj = await uow.users.create_one(data=user_dict)
            await uow.commit()
            return user_obj.model_dump(exclude=["password", "id"]), None

    @staticmethod
    async def login_user(uow: IUnitOfWork, user: UserLogin) -> tuple[dict[str | Any], Error]:
        async with uow:
            user_obj = await uow.users.read_one(login=user.login)
            if user_obj:
                if check_password_hash(user_obj.password, user.password):
                    user_token = await uow.tokens.get_user_token(user_id=user_obj.id)
                    await uow.commit()
                    return user_token.model_dump(
                        include=["user_id", "access_token", "refresh_token"]
                    ), None
                else:
                    return {}, "incorrect_password"
            else:
                return {}, "user_not_exist"

    @staticmethod
    async def get_all(uow: IUnitOfWork):
        async with uow:
            users = await uow.users.get_all()
            return users

