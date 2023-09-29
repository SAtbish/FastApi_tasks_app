from src.models.tasks_attachments import TaskAttachments
from src.utils.repository import SQLAlchemyRepository


class TaskAttachmentsRepository(SQLAlchemyRepository):
    model = TaskAttachments
