from typing import Optional

from fasttower.auth import hashers
from pydantic import EmailStr
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True)
    username: str = Field(unique=True, max_length=50)
    name: Optional[str] = Field(max_length=100, nullable=True)
    surname: Optional[str] = Field(max_length=100, nullable=True)
    password_hash: Optional[str] = Field(max_length=256)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)

    @property
    def password(self) -> str:
        return self.password_hash

    @password.setter
    def password(self, value):
        self.password_hash = hashers.hash_password(value)

    def verify_password(self, password: str) -> bool:
        return hashers.check_password(self.password_hash, password)
