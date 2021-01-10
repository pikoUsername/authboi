import asyncio

from aiogram import Dispatcher
from aiogram.utils.executor import Executor
from loguru import logger

from ..models.user import User
from ..models import base
from .. import config
from ..loader import dp


runner = Executor(dp)


async def on_startup_webhook(dispatcher: Dispatcher):
    logger.info("Configure Web-Hook URL to: {url}", url=config.WEBHOOK_URL)
    await dispatcher.bot.set_webhook(config.WEBHOOK_URL)


async def notify_admins(dp_: Dispatcher):
    all_admins = await User.query.where(User.is_admin is True).gino.all()
    for user in all_admins:
        await dp_.bot.send_message(
            chat_id=user.user_id, text="Bot started", disable_notification=True
        )
        logger.info("Notified superuser {user} about bot is started.", user=user.id)
        await asyncio.sleep(0.2)


def setup():
    base.setup(runner)
    logger.info("Configure executor...")
    runner.on_startup(on_startup_webhook, webhook=True, polling=False)
    if config.ON_STARTUP_NOTIFY:
        runner.on_startup(notify_admins)
