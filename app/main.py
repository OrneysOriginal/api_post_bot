from fastapi import FastAPI

from app.admin.router import admin_router
from app.tg_bot.router import bot_router

app = FastAPI()


@app.get("/health/")
def health_check():
    return {"status": "healthy"}


app.include_router(
    admin_router,
)

app.include_router(
    bot_router,
)
