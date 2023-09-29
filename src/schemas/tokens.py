from datetime import datetime

from pydantic import BaseModel


class TokensSchema(BaseModel):
    id: int
    access_token: str
    refresh_token: str
    data_time: datetime
    user_id: int
    is_permanent: bool
