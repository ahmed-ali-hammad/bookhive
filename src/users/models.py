from datetime import date, datetime

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: int = Field(default=None, primary_key=True, nullable=False) 
    username: str
    email: str
    first_name: str = Field(nullable=True) 
    last_name: str = Field(nullable=True) 
    password_hash: str = Field(exclude=True)
    is_verified: bool = False
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f"User {self.first_name} {self.last_name}"
