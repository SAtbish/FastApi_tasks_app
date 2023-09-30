from typing import Any

from src.enums import Error
from src.schemas.users import UserRegistration, UserLogin
from src.utils.unitofwork import IUnitOfWork
from werkzeug.security import generate_password_hash, check_password_hash


class UsersService:
    @staticmethod
    async def get_user(uow: IUnitOfWork, user_info: dict[str, Any]):
        async with uow:
            user = await uow.users.read_one(**user_info)
            if not user:
                return None, "user_not_exist"
            else:
                return user.to_read_model(), None

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

    @staticmethod
    async def delete_user_by_id(uow: IUnitOfWork, user_id: int):
        async with uow:
            deleted_tokens_ids = [del_id[0] for del_id in await uow.tokens.delete(user_id=user_id)]
            deleted_tasks_ids = [del_id.id for del_id in await uow.tasks.get_all(author_id=user_id)]
            deleted_tasks_ids += [del_id.id for del_id in await uow.tasks.get_all(assignee_id=user_id)]
            deleted_tasks_ids = set(deleted_tasks_ids)
            for task_id in deleted_tasks_ids:
                await uow.tasks_attachments.delete(task_id=task_id)
                await uow.tasks.delete_one_by_id(obj_id=task_id)
            deleted_notifications_ids = [del_id[0] for del_id in await uow.notifications.delete(user_id=user_id)]
            deleted_user_id = await uow.users.delete_one_by_id(obj_id=user_id)
            await uow.commit()
            return {
                "deleted_user_id": deleted_user_id,
                "deleted_tokens_ids": deleted_tokens_ids,
                "deleted_tasks_ids": deleted_tasks_ids,
                "deleted_notifications_ids": deleted_notifications_ids
            }
