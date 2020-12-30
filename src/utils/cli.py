import datetime
import asyncio

from aiogram import Dispatcher
from loguru import logger

from . import log
from ..models.base import create_db, close_db
from ..loader import bot, telegraph


async def on_startup(dp: Dispatcher):
    from src import middlewares

    await asyncio.sleep(2)

    log.setup()
    middlewares.setup(dp)
    await create_db()

    logger.info(f"Bot started | time: {datetime.datetime.today()}")

    from src.handlers.admins.notify_admins import notify_admins
    await notify_admins(dp)


async def on_shutdown(dp):
    logger.info("Goodbye!.")
    await telegraph.close()
    await bot.close()
    await close_db()


def start_bot():
    from aiogram import executor
    from src.handlers import dp

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
