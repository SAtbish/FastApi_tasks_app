from src.enums import Error
from src.schemas.users import UserRegistration
from src.utils.unitofwork import IUnitOfWork
from werkzeug.security import generate_password_hash


class UsersService:
    @staticmethod
    async def create_user(uow: IUnitOfWork, user: UserRegistration) -> tuple[int, Error]:
        async with uow:
            # checking for login existence
            exist_login = await uow.users.read_one(login=user.login)
            if exist_login:
                return 0, "login_exist"

            # checking for email existence
            exist_email = await uow.users.read_one(email=user.email)
            if exist_email:
                return 0, "email_exist"

            user.password = generate_password_hash(user.password)
            user_dict = user.model_dump()

            user_id = await uow.users.create_one(data=user_dict)
            await uow.commit()
            return user_id, None
