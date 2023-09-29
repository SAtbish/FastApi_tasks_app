from abc import ABC, abstractmethod
from typing import Type

from src.db.db import async_session_maker
from src.repositories.notification_types import NotificationTypesRepository
from src.repositories.notifications import NotificationsRepository
from src.repositories.users import UsersRepository
from src.repositories.tasks import TasksRepository
from src.repositories.tasks_attachments import TaskAttachmentsRepository
from src.repositories.tokens import TokensRepository


class IUnitOfWork(ABC):
    users: Type[UsersRepository]
    tasks: Type[TasksRepository]
    tasks_attachments: Type[TaskAttachmentsRepository]
    tokens: Type[TokensRepository]
    notifications: Type[NotificationsRepository]
    notification_types: Type[NotificationTypesRepository]

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UsersRepository(self.session)
        self.tasks = TasksRepository(self.session)
        self.tasks_attachments = TaskAttachmentsRepository(self.session)
        self.tokens = TokensRepository(self.session)
        self.notifications = NotificationsRepository(self.session)
        self.notification_types = NotificationTypesRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
