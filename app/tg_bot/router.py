from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.models import PostModel
from app.database import get_async_session

bot_router = APIRouter(
    prefix="/bot",
    tags=["bot"],
)


@bot_router.get("/get_posts/")
async def get_posts(session: AsyncSession = Depends(get_async_session)) -> dict:
    query = select(PostModel)
    data = await session.execute(query)
    posts = [post.header for post in data.scalars().all()]
    return {"status_code": 200, "content": posts}


@bot_router.get("/get_post/{header}")
async def get_post(
    header: str, session: AsyncSession = Depends(get_async_session)
) -> dict:
    query = select(PostModel).filter(PostModel.header == header)
    data = await session.execute(query)
    post = data.scalar()
    if post is None:
        return {"status_code": 404, "info": "Post not found"}
    msg = f"{post.text}\n\n{post.created_at}"
    return {"status_code": 200, "msg": msg}
