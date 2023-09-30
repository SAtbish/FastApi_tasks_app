from datetime import datetime
from pydantic import BaseModel


class TasksSchema(BaseModel):
    id: int
    title: str
    author_id: int
    assignee_id: int
    creation_date: datetime
    expiration_date: datetime
    is_done: bool
    done_date: datetime
