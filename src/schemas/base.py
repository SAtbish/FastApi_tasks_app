from typing import Any

from pydantic import BaseModel


class ResponseModel(BaseModel):
    message: str | None = None
    data: dict[str, Any] | None = None
