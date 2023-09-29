from src.models.tasks import Tasks
from src.utils.repository import SQLAlchemyRepository


class TasksRepository(SQLAlchemyRepository):
    model = Tasks
