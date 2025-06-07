import requests
from aiogram import Router
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from aiogram.filters import Command
from app.config import WEB_HOST, WEB_PORT

router = Router()


@router.message(Command("posts"))
async def message_handler(msg: Message):
    url = f"http://{WEB_HOST}:{WEB_PORT}/bot/get_posts/"
    response = requests.get(url)
    result = response.json().get("content")
    for i in range(len(result)):
        result[i] = [InlineKeyboardButton(text=result[i], callback_data=result[i])]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=result)
    await msg.answer("Посты:", reply_markup=inline_keyboard)


@router.callback_query()
async def inline_buttons_handle(callback: CallbackQuery):
    header = callback.data
    url = f"http://{WEB_HOST}:{WEB_PORT}/bot/get_post/{header}"
    response = requests.get(url)
    data = response.json()
    if data.get("status_code") != 200:
        await callback.message.answer("Это пост был удалён")
    msg = data.get("msg")
    await callback.message.answer(msg)
