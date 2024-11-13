import datetime
from typing import Optional

from fasttower.auth import hashers
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship


class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)

    users: list["User"] = Relationship(back_populates="role")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True)
    username: str = Field(unique=True, max_length=50)
    name: Optional[str] = Field(max_length=100, nullable=True)
    surname: Optional[str] = Field(max_length=100, nullable=True)
    password_hash: Optional[str] = Field(max_length=256)
    is_active: bool = Field(default=True)

    role_id: int | None = Field(default=None, foreign_key="role.id")
    role: Role | None = Relationship(back_populates="users")

    # связь с тасками
    tasks: list["Task"] = Relationship(back_populates="user")

    @property
    def password(self) -> str:
        return self.password_hash

    @password.setter
    def password(self, value):
        self.password_hash = hashers.hash_password(value)

    def verify_password(self, password: str) -> bool:
        return hashers.check_password(self.password_hash, password)


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str = Field(max_length=100, unique=True)
    topic: str = Field(max_length=100, unique=True)
    data_creation: datetime.date = Field(default_factory=datetime.date.today)
    date_from: datetime.date = Field(default_factory=datetime.date.today)
    date_to: datetime.date = Field(default_factory=datetime.date.today)

    user_id: Optional[int] = Field(foreign_key="user.id")
    user: User | None = Relationship(back_populates="tasks")
