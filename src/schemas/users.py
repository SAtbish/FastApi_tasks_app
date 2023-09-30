from pydantic import BaseModel, Field, EmailStr, constr

from src.schemas.base import ResponseModel


class UserInfoModel(BaseModel):
    name: str | None = None
    login: str | None = None
    email: str | None = None


class UserInfo(UserInfoModel):
    is_confirmed: bool


class UserSchema(UserInfo):
    id: int
    password: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    login: str = Field(min_length=1, max_length=64, description="User login")
    password: constr(pattern="^[A-Za-z0-9-!№;$%^&*():?/|.,~`]+$", min_length=8, max_length=64)


class UserRegistration(UserLogin):
    name: str = Field(min_length=1, max_length=64, description="User name")
    email: EmailStr


class UserResponseModel(ResponseModel):
    data: UserInfo


class UsersResponseModel(ResponseModel):
    data: list[UserInfo]


class GetUserRequest(BaseModel):
    name: str | None = None
    login: str | None = None
    email: str | None = None
    is_confirmed: bool | None = None

    def get_not_none_values(self):
        return self.model_dump()


class UserDeletionInfo(BaseModel):
    deleted_user_id: int
    deleted_tokens_ids: list[int]
    deleted_tasks_ids: list[int]
    deleted_notifications_ids: list[int]
