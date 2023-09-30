from pydantic import BaseModel, Field, EmailStr, constr

from src.schemas.base import ResponseModel


class UserResponse(BaseModel):
    name: str
    login: str
    email: str
    is_confirmed: bool


class UserSchema(UserResponse):
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
    data: UserResponse


class UsersResponseModel(ResponseModel):
    data: list[UserResponse]


class GetUserRequest(BaseModel):
    name: str | None = None
    login: str | None = None
    email: str | None = None
    is_confirmed: bool | None = None

    def get_not_none_values(self):
        return self.model_dump()
