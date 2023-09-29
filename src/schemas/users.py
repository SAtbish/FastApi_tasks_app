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
