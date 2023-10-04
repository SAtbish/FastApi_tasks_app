import hashlib
from typing import Any

from src.enums import Error
from src.schemas.users import UserRegistration, UserLogin
from src.utils.notifications import make_confirm_email_notification
from src.utils.redis import save_notification_to_redis
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
    async def check_login(uow: IUnitOfWork, login: str):
        async with uow:
            return await uow.users.read_one(login=login)

    @staticmethod
    async def check_email(uow: IUnitOfWork, email: str):
        async with uow:
            return await uow.users.read_one(email=email)

    async def create_user(self, uow: IUnitOfWork, user: UserRegistration) -> tuple[dict[str | Any], Error]:
        if await self.check_login(uow, user.login):
            return {}, "login_exist"
        if await self.check_email(uow, user.email):
            return {}, "email_exist"
        async with uow:
            user.password = generate_password_hash(user.password)
            user_dict = user.model_dump()

            user_obj = await uow.users.create_one(data=user_dict)
            (not_saved, err) = await save_notification_to_redis(
                make_confirm_email_notification(user_id=user_obj.id, email=user_obj.email)
            )
            if not_saved:
                return {}, err
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
    async def get_all_paginated(uow: IUnitOfWork):
        async with uow:
            users = await uow.users.get_all_paginated()
            return users

    async def update_user_info(self, uow: IUnitOfWork, user_id: int, user_info: dict):
        if user_info.get("login") and await self.check_login(uow, user_info.get("login")):
            return {}, "login_exist"
        if user_info.get("email") and await self.check_email(uow, user_info.get("email")):
            return {}, "email_exist"
        async with uow:
            user = await uow.users.update_one(obj_id=user_id, data=user_info)
            await uow.commit()
            return user, None

    @staticmethod
    async def update_user_password(uow: IUnitOfWork, user_id: int, old_password: str, new_password: str):
        async with uow:
            user = await uow.users.read_one(id=user_id)
            if not user:
                return {}, "user_not_exist"

            if check_password_hash(user.password, old_password):
                user = await uow.users.update_one(
                    obj_id=user_id,
                    data={
                        "password": generate_password_hash(new_password)
                    }
                )
                await uow.commit()
                return user, None
            else:
                return {}, "incorrect_password"

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

    async def confirm_user_email(self, uow: IUnitOfWork, user_info: dict[str, Any], email_hash: str):
        async with uow:
            user, err = await self.get_user(uow, user_info)
            if err:
                return err
            if not user.is_confirmed:
                if email_hash == hashlib.md5(bytes(user.email, "utf-8")).hexdigest():
                    await self.update_user_info(uow, user_id=user.id, user_info={"is_confirmed": True})
                else:
                    return "wrong_email"
            else:
                return "already_confirmed"
