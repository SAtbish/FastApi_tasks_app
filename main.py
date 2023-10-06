import re

from starlette.requests import Request
import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.services.notifications_types import NotificationsTypesService
from src.utils.unitofwork import UnitOfWork
from src.utils.user_authorization import user_authorization
from src.redis_worker.redis_worker import r
from src.tasks.celery_worker import celery_app
from multiprocessing import Process
from subprocess import Popen

NOT_AUTHORIZATION_PATTERNS = [
    "/",
    "/docs",
    "/openapi.json",
    "/users/registration",
    "/users/login",
    r"^/users/confirm/email/\d+/[0-9A-Za-z]+$"
]

app = FastAPI(
    title="Приложение для ведения задач пользователей"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
add_pagination(app)


@app.on_event("startup")
async def startup_event():
    FastAPICache.init(RedisBackend(r), prefix="fastapi-cache")
    await NotificationsTypesService.create_notification_types(uow=UnitOfWork())


@app.middleware("http")
async def add_authorization(request: Request,  call_next):
    tokens = {}
    if not any([re.fullmatch(pattern, request.url.path) for pattern in NOT_AUTHORIZATION_PATTERNS]):
        tokens, err = await user_authorization(request)
        if not tokens:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'message': err})

    response = await call_next(request)
    if tokens:
        for key, value in tokens.items():
            response.set_cookie(key, value)

    return response

if __name__ == "__main__":
    celery_worker_process = Process(target=celery_app.worker_main,
                                    kwargs={"argv": ["worker", "--loglevel=info", "--pool=solo", "-E"]})
    celery_worker_process.start()
    celery_beat_process = Popen(["celery", "--app", "src.tasks.celery_worker", "beat", "--loglevel=info"])
    uvicorn.run(app="src.api:app", reload=True)
