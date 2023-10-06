from src.api.tasks.router import router
from fastapi import status

from src.schemas.base import ResponseModel
from src.schemas.tasks import CreateTasks, TaskResponse, TaskData
from src.api.dependencies import UOWDep
from src.services.tasks import TasksService
from src.utils.create_response import create_response


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    description=(
            "Создаёт задачу\n\n"
            "Create task"
    ),
    summary="create task",
    response_model=TaskResponse,
    responses={
        status.HTTP_201_CREATED: {
            "model": TaskResponse,
            "description": "Got user",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ResponseModel,
            "description": "User not authorized. Check message",
        },
        status.HTTP_409_CONFLICT: {
            "model": ResponseModel,
            "description": "Can not find user. Check message",
        }
    }
)
async def create_task_handler(
        task_info: CreateTasks,
        uow: UOWDep
):
    task, err = await TasksService().create_task(uow, task_info)
    if err:
        return create_response(
            content=ResponseModel(message=err),
            status=status.HTTP_409_CONFLICT
        )
    return create_response(
        content=TaskResponse(data=TaskData(**task)),
        status=status.HTTP_201_CREATED
    )
