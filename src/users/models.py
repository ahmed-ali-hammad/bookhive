from datetime import datetime
from typing import List

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, Relationship, SQLModel, String


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: int = Field(default=None, primary_key=True, nullable=False)
    username: str
    email: str
    first_name: str = Field(nullable=True)
    last_name: str = Field(nullable=True)
    password_hash: str = Field(exclude=True)
    is_verified: bool = False
    role: str = Field(sa_column=Column(String, nullable=False, server_default="user"))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    books: List["Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    reviews: List["Review"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"User {self.first_name} {self.last_name}"
