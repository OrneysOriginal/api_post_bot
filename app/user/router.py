import secrets

from fastapi import APIRouter, Depends, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.user.auth import create_access_token
from app.user.models import UserModel, hashed_password, verify_password
from app.user.schemas import SRegistration, SLogin

user_router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@user_router.post("/register/")
async def registration(
    data: SRegistration, session: AsyncSession = Depends(get_async_session)
):
    if not secrets.compare_digest(data.password, data.repeat_password):
        return {
            "status_code": 412,
            "info": "Password and repeatable password dont match",
        }
    query = select(UserModel).filter(UserModel.username == data.username)
    required_user = await session.execute(query)
    required_user = required_user.scalar_one_or_none()
    if required_user is not None:
        return {
            "status_code": 409,
            "info": "User with this username already registered",
        }
    hashed_pwd = hashed_password(data.password)
    user = UserModel(username=data.username, hash_password=hashed_pwd)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return {"status_code": 200}


@user_router.post("/login/")
async def login(
    response: Response,
    data: SLogin,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    user, err = await authenticate(data, session)
    if user is None:
        return err

    access_token = await create_access_token({"user": str(user.id)})
    response.set_cookie("user_access_token", access_token, httponly=True)
    return {"access_token": access_token}


async def authenticate(
    data: SLogin = Depends(), session: AsyncSession = Depends(get_async_session)
) -> tuple:
    query = select(UserModel).filter(UserModel.username == data.username)
    user = await session.execute(query)
    user = user.scalar_one_or_none()
    if user is None:
        return None, {"status_code": 404, "info": "User with this username - not found"}

    if verify_password(user.hash_password, hashed_password(data.password)):
        return None, {"status_code": 412, "info": "Incorrect password"}

    return user, None
