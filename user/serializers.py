from pydantic import BaseModel, EmailStr


class UserSerializer(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserCreateSerializer(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLoginSerializer(BaseModel):
    username: str
    password: str


class JWTDataSerializer(BaseModel):
    id: int
    sub: str


class JWTSerializer(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
