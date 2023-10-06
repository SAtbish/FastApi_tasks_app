from pydantic import Field
from datetime import datetime
from pydantic import BaseModel, field_validator

from src.schemas.base import ResponseModel


class CreateTasks(BaseModel):
    title: str = Field(min_length=1, max_length=64, description="Task title")
    author_id: int = Field(gt=0, description="Task author")
    assignee_id: int = Field(gt=0, description="Task assignee")
    expiration_date: datetime | None = None
    is_done: bool | None = False
    done_date: datetime | None = None

    @field_validator('expiration_date', 'done_date')
    def name_must_contain_space(cls, date: datetime) -> datetime:
        return date.replace(tzinfo=None)


class TaskData(CreateTasks):
    creation_date: datetime


class TaskResponse(ResponseModel):
    data: TaskData


class TasksSchema(TaskData):
    id: int
