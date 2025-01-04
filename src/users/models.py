from datetime import date, datetime
from uuid import UUID

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: UUID = Field(primary_key=True)
    username: str
    email: str
    first_name: str
    last_name: date
    is_verified: bool = False
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f"User {self.first_name} {self.last_name}"
