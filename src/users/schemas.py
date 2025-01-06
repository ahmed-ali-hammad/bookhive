from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional


class UserModel(BaseModel):
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserCreateModel(BaseModel):
    username: str = Field(max_length=10)
    email: EmailStr
    password: str


class UserAuthModel(BaseModel):
    email: EmailStr
    password: str
