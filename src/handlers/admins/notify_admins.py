from aiogram import Dispatcher
from loguru import logger

from src.loader import bot
from src.data.config import ADMIN_IDS

async def notify_admins(dp: Dispatcher):
    for admins in ADMIN_IDS:
        try:
            await bot.send_message(chat_id=admins, text="Бот запущен")
        except Exception as e:
            logger.exception(f"Untracked ERROR! {e}")