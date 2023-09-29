from src.models.notifications import Notifications
from src.utils.repository import SQLAlchemyRepository


class NotificationsRepository(SQLAlchemyRepository):
    model = Notifications
