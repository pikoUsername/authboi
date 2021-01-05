import asyncio

from aiogram import Dispatcher
from aiogram.utils.executor import Executor
from loguru import logger

from ..models import User
from ..models import base
from .. import config
from ..loader import dp


runner = Executor(dp)


async def notify_admins(dp: Dispatcher):
    all_admins = await User.query.where(User.is_admin == True).gino.all()
    for user in all_admins:
        await dp.bot.send_message(
            chat_id=user.user_id, text="Bot started", disable_notification=True
        )
        logger.info("Notified superuser {user} about bot is started.", user=user.id)
        await asyncio.sleep(0.2)


def setup():
    base.setup(runner)
    logger.info("Configure executor...")
    if config.ON_STARTUP_NOTIFY:
        runner.on_startup(notify_admins)
