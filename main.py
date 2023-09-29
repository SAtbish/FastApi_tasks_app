import uvicorn
from fastapi import FastAPI


app = FastAPI(
    title="Приложение для ведения задач пользователей"
)


if __name__ == "__main__":
    uvicorn.run(app="src.api:app", reload=True)
