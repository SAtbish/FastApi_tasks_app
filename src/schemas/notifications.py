from datetime import datetime

from pydantic import BaseModel


class NotificationRedisModel(BaseModel):
    header: str
    message: str
    type: str
    user_id: int


class NotificationSchema(NotificationRedisModel):
    id: int
    sent_datetime: datetime
