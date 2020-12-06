from loguru import logger

from src.models.models import create_db
from src.loader import bot

async def on_startup(dp):
    from src import filters
    from src import middlewares
    from src.handlers import user, errors

    errors.setup(dp)
    user.setup(dp)
    filters.setup(dp)
    middlewares.setup(dp)
    await create_db()

    logger.info("Bot started")

    from src.handlers.admins.notify_admins import notify_admins
    await notify_admins(dp)

async def on_shutdown(dp):
    logger.info("Goodbye, mother fucker)!.")
    await bot.close()


if __name__ == '__main__':
    from aiogram import executor
    from src.loader import dp

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)