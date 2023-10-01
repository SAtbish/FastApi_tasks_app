from celery import Celery
from src.tasks.notifications_tasks import insert_notifications_to_database
import asyncio
from config import REDIS_HOST, REDIS_PORT, REDIS_DB


celery_app = Celery("celery_app", broker=f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")


@celery_app.task()
def insert_notifications_task():
    asyncio.get_event_loop().run_until_complete(insert_notifications_to_database())


celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Moscow",
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    "call-send_email-task-every-15-seconds": {
        "task": "src.tasks.celery_worker.insert_notifications_task",
        "schedule": 15.0,
    }
}
