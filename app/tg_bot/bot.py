import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from app.config import TG_BOT_TOKEN
from app.tg_bot.handlers import router


async def set_main_menu(bot: Bot):
    main_menu_command = [
        BotCommand(command="/posts", description="Show all posts"),
    ]
    await bot.set_my_commands(main_menu_command)


async def main():
    bot = Bot(
        token=TG_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.startup.register(set_main_menu)
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


asyncio.run(main())
