from datetime import datetime
from src.schemas.notifications import NotificationRedisModel
from src.utils.unitofwork import IUnitOfWork


class NotificationsService:
    @staticmethod
    async def create_notification(uow: IUnitOfWork, notification: NotificationRedisModel):
        async with uow:
            new_notification = await uow.notifications.create_one(
                data={**notification.model_dump(), "sent_datetime": datetime.now()}
            )
            await uow.commit()
            return new_notification.model_dump(exclude=["id"]), None
