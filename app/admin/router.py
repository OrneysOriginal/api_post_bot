import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.models import PostModel
from app.admin.schemas import SUpdatePost, SPost
from app.database import get_async_session


admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@admin_router.post("/create_post/")
async def create_post(
    data: SPost, session: AsyncSession = Depends(get_async_session)
) -> dict:
    query = select(PostModel).filter(PostModel.header == data.header)
    post = await post_is_exists(query, session)
    if post is not None:
        return {"status_code": 409, "info": "Post is exists"}

    new_post = PostModel(
        header=data.header, text=data.text, created_at=datetime.datetime.now()
    )
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)
    return {"status_code": 200, "info": "Successful added"}


@admin_router.patch("/update_post/{post_id}")
async def update_post(
    post_id: int, data: SUpdatePost, session: AsyncSession = Depends(get_async_session)
) -> dict:
    query = select(PostModel).filter(PostModel.id == post_id)
    post = await post_is_exists(query, session)
    if post is None:
        return {"status_code": 404, "info": "Post not found"}

    updated_data = data.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(post, key, value)

    await session.commit()
    return {"status_code": 200, "info": "Successful updated"}


@admin_router.delete("/delete_post/{post_id}")
async def delete_post(
    post_id: int, session: AsyncSession = Depends(get_async_session)
) -> dict:
    query = select(PostModel).filter(PostModel.id == post_id)
    post = await post_is_exists(query, session)
    if post is None:
        return {"status_code": 404, "info": "Post not found"}

    await session.delete(post)
    await session.commit()
    return {"status_code": 200, "info": "Successful deleted"}


async def post_is_exists(query, session: AsyncSession) -> None:
    post = await session.execute(query)
    post = post.scalar()
    return post
