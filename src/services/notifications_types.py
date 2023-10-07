from src.utils.unitofwork import IUnitOfWork


class NotificationsTypesService:
    @staticmethod
    async def create_notification_types(uow: IUnitOfWork):
        async with uow:
            result = await uow.notification_types.get_all()
            if not result:
                await uow.notification_types.create_one(
                    data={"type": "confirm_email", "description": "confirm email"}
                )
                await uow.notification_types.create_one(
                    data={"type": "new_task", "description": "new task"}
                )
            await uow.commit()
