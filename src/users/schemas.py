from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserModel(BaseModel):
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_verified: bool
    role: str
    created_at: datetime
    updated_at: datetime


class UserCreateModel(BaseModel):
    username: str = Field(max_length=10)
    email: EmailStr
    password: str


class UserAuthModel(BaseModel):
    email: EmailStr
    password: str
