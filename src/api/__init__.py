from src.api.index import app
from src.api.users import router
from src.api.routers import all_routers

for router in all_routers:
    app.include_router(router)

__all__ = ["app"]
