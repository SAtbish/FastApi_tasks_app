from src.enums import Error
from src.redis_worker.redis_worker import rw, check_availability, REDIS_NAME
from config import REDIS_NOTIFICATIONS_KEY
from src.schemas.notifications import NotificationRedisModel


async def save_notification_to_redis(notification: NotificationRedisModel) -> tuple[bool, Error]:
    if not await check_availability():
        return True, "redis_server_dead"

    before_keys = await rw.r.keys(f"{REDIS_NAME}:{REDIS_NOTIFICATIONS_KEY}:list")
    before_notifications = await rw.get_redis(before_keys)
    if before_notifications:
        notifications = before_notifications[f'{REDIS_NOTIFICATIONS_KEY}']
    else:
        notifications = []

    await rw.income_notifications.set(notifications + [notification.model_dump()])

    return False, None


