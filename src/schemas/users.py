from pydantic import BaseModel, Field, EmailStr, constr


class UserSchema(BaseModel):
    id: int
    name: str
    login: str
    password: str
    email: str
    is_confirmed: bool

    class Config:
        from_attributes = True


class UserRegistration(BaseModel):
    name: str = Field(min_length=1, max_length=64, description="User name")
    login: str = Field(min_length=1, max_length=64, description="User login")
    password: constr(pattern="^[A-Za-z0-9-!№;$%^&*():?/|.,~`]+$", min_length=8, max_length=64)
    email: EmailStr
