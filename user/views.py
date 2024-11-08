from typing import Annotated

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fasttower.conf import settings
from fasttower.routers import APIRouter
from fasttower.utils import get_user_model
from jwt import InvalidTokenError
from starlette import status

from TestFastTower.database import SessionDep
from user.serializers import UserSerializer, UserCreateSerializer, JWTSerializer, TokenData, \
    JWTDataSerializer
from user.utils import get_user, create_tokens

User = get_user_model()
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login", )


@router.post('/create', response_model=UserSerializer)
async def create_user(user: UserCreateSerializer, session: SessionDep):
    user_ = User(email=user.email, username=user.username)
    user_.password = user.password
    session.add(user_)
    await session.commit()
    await session.refresh(user_)
    return user_


@router.post('/login')
async def login(user: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep) -> JWTSerializer:
    user_ = await get_user(user.username, session)
    print(user_)
    if not user_ or not user_.verify_password(user.password):
        raise HTTPException(status_code=404, detail="User not found")

    tokens = create_tokens(JWTDataSerializer(id=user_.id, sub=user_.username).model_dump())
    return JWTSerializer(access_token=tokens["access"], refresh_token=tokens["refresh"], token_type="bearer")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.AUTH['ALGORITHM']])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(token_data.username, session)
    if user is None:
        raise credentials_exception
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("/me", response_model=UserSerializer)
async def read_users_me(
        current_user: CurrentUser,
):
    return current_user
