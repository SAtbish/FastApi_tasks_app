import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from src.redis_worker.redis_worker import r
from src.tasks.celery_worker import celery_app
from multiprocessing import Process
from subprocess import Popen


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


if __name__ == "__main__":
    celery_worker_process = Process(target=celery_app.worker_main,
                                    kwargs={"argv": ["worker", "--loglevel=info", "--pool=solo", "-E"]})
    celery_worker_process.start()
    celery_beat_process = Popen(["celery", "--app", "src.tasks.celery_worker", "beat", "--loglevel=info"])
    uvicorn.run(app="src.api:app", reload=True)
