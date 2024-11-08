from datetime import datetime, timezone, timedelta

import jwt
from fasttower.conf import settings
from fasttower.utils import get_user_model
from sqlalchemy import select

from TestFastTower.database import SessionDep

User = get_user_model()


def create_token(data: dict, expires_delta: timedelta | None = None, type_: str = "access"):
    if expires_delta is None:
        expires_delta = settings.AUTH[type_.upper()]
    return jwt.encode({"exp": datetime.now(timezone.utc) + expires_delta,
                       "type": type_, **data.copy()},
                      settings.SECRET_KEY, algorithm=settings.AUTH['ALGORITHM'])


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    return create_token(data, expires_delta, type_="access")


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    return create_token(data, expires_delta, type_="refresh")


def create_tokens(data: dict, access_delta: timedelta | None = None, refresh_delta: timedelta | None = None): \
        return {
            "access": create_access_token(data, access_delta),
            "refresh": create_refresh_token(data, refresh_delta)
        }


async def get_user(username: str, session: SessionDep):
    return (await session.execute(select(User).filter_by(username=username))).fetchone()[0]
