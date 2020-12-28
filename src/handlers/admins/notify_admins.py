import asyncio
from contextlib import suppress

from aiogram import Dispatcher
from aiogram.utils.exceptions import TelegramAPIError
from loguru import logger

from ...models import models


async def notify_admins(dp: Dispatcher):
    all_admins = await models.User.query.where(models.User.is_admin==True).gino.all()
    for user in all_admins:
        await dp.bot.send_message(
            chat_id=user.user_id, text="Bot started", disable_notification=True
        )
        logger.info("Notified superuser {user} about bot is started.", user=user.id)
        await asyncio.sleep(0.2)
