import datetime
import asyncio

from loguru import logger

from src.utils import log
from src.models.models import create_db
from src.loader import bot

async def on_startup(dp):
    from src import filters
    from src import middlewares
    
    await asyncio.sleep(2)

    log.setup()
    filters.setup(dp)
    middlewares.setup(dp)
    await create_db()

    logger.info(f"Bot started | time: {datetime.datetime.today()}")

    from src.handlers.admins.notify_admins import notify_admins
    await notify_admins(dp)

async def on_shutdown(dp):
    logger.info("Goodbye!.")
    await bot.close()

if __name__ == '__main__':
    from aiogram import executor
    from src.handlers import dp

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
