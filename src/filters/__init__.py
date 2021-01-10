from aiogram import Dispatcher
from loguru import logger

from .auth import AuthRequired


def setup(dp: Dispatcher):
    logger.info("Setuping Filters...")

    dp.filters_factory.bind(AuthRequired, event_handlers=[
        dp.message_handlers,
        dp.edited_message_handlers,
        dp.channel_post_handlers,
        dp.edited_channel_post_handlers,
    ])