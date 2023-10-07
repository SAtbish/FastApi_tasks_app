import json
from datetime import datetime
from fastapi.responses import JSONResponse
from src.schemas.base import ResponseModel


def json_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f'Type {type(obj)} is not serializable')


def create_response(content: ResponseModel, status: int):
    content_data = json.dumps(content.model_dump(), default=json_serializer)
    return JSONResponse(content=json.loads(content_data), status_code=status)
