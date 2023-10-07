from datetime import datetime
from src.schemas.tasks import CreateTasks
from src.utils.notifications import make_new_task_notification
from src.utils.redis import save_notification_to_redis
from src.utils.unitofwork import IUnitOfWork


class TasksService:
    @staticmethod
    async def create_task(uow: IUnitOfWork, task: CreateTasks):
        async with uow:
            is_exist = await uow.users.read_one(id=task.author_id)
            if not is_exist:
                return {}, "author_not_exist"

            asignee = await uow.users.read_one(id=task.assignee_id)
            if not asignee:
                return {}, "assignee_not_exist"

            new_task = await uow.tasks.create_one(
                data={**task.model_dump(), "creation_date": datetime.now()}
            )

            (not_saved, err) = await save_notification_to_redis(
                make_new_task_notification(user_id=task.assignee_id)
            )
            if not_saved:
                return {}, err

            await uow.commit()
            return new_task.model_dump(exclude=["id"]), None
