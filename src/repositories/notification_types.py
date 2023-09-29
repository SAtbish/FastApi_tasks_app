from src.models.notification_types import NotificationTypes
from src.utils.repository import SQLAlchemyRepository


class NotificationTypesRepository(SQLAlchemyRepository):
    model = NotificationTypes
