from src.api.users.router import router as users_router
from src.api.tasks.router import router as tasks_router

all_routers = [
    users_router,
    tasks_router
]
