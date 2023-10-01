from src.redis_worker.redis_worker import rw
from src.schemas.notifications import NotificationRedisModel
from src.services.notifications import NotificationsService
from src.services.users import UsersService
from src.utils.email_worker import send_message_to_email
from src.utils.redis import get_notifications_from_redis
from src.utils.unitofwork import UnitOfWork


async def insert_notifications_to_database():
    income_notifications = [
        NotificationRedisModel(**notification)
        for notification in await get_notifications_from_redis() if isinstance(notification, dict)
    ]

    uow = UnitOfWork()
    for notification in income_notifications:
        async with uow:
            user, err = await UsersService().get_user(uow, user_info={"id": notification.user_id})
            if not err:
                await NotificationsService().create_notification(uow, notification)
                await send_message_to_email(notification=notification, user_email=user.email)
    await rw.income_notifications.set([])



