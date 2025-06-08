from datetime import datetime, timezone

import jwt
from fastapi import Request, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import SECRET_KEY, ALGORITHM
from app.database import get_async_session
from jose import JWTError

from app.user.models import UserModel


def get_token(request: Request) -> str:
    token = request.cookies.get("user_access_token")
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found"
        )
    return token


async def check_auth_user(
    token: str = Depends(get_token), session: AsyncSession = Depends(get_async_session)
):
    try:
        token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return False

    expire = token.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if expire is None or expire_time < datetime.now(timezone.utc):
        return False

    user_id = token.get("user")
    if user_id is None:
        return False

    query = select(UserModel).filter(UserModel.id == int(user_id))
    user = await session.execute(query)
    user = user.scalar_one_or_none()
    if user is None:
        return False

    return True
