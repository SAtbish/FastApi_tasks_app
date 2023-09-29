from main import app
from fastapi.responses import JSONResponse
from fastapi import status
from src.schemas.base import ResponseModel
from datetime import datetime

route_description = {
    'response_model': ResponseModel,
    'status_code': status.HTTP_200_OK,
    'tags': ["index"],
    'description': (
        "Проверяет доступно ли приложение\n\n"
        "Check availability of application"
    ),
    'summary': "Check app",
}


@app.get("/", **route_description)
@app.get("/ping", **route_description)
async def index_handler():
    return JSONResponse(
        content=ResponseModel(message=f"{datetime.now()}: Working...").__dict__,
        status_code=status.HTTP_200_OK
    )
