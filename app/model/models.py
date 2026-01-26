from pydantic import BaseModel, EmailStr, Field
from enum import Enum
import secrets

class Gender(str, Enum):
    male = "male"
    female = "female"

from pydantic import BaseModel

class UpdateType(str,Enum):
    email = "email"
    username = "username"
    password = "password"

class UserRegister(BaseModel):
    username: str
    email: EmailStr | None = None
    password: str
    age: int
    gender: Gender
    country: str
    region: str


class User(BaseModel):
    username: str
    email: EmailStr | None = None
    password: str
    

class UserUpdate(BaseModel):
    updateType: UpdateType
    username: str | None = None
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=3, max_length=128)

class UserLogout(BaseModel):
    username: str

class UserToDelete(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    refresh_token: str