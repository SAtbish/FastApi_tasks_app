import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination


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

if __name__ == "__main__":
    uvicorn.run(app="src.api:app", reload=True)
