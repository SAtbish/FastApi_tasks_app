from fastapi.responses import JSONResponse

from src.schemas.base import ResponseModel


def create_response(content: ResponseModel, status: int):
    return JSONResponse(content=content.model_dump(), status_code=status)
