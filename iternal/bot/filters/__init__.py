from aiogram import Dispatcher
from loguru import logger

from .auth import AuthRequired
from .admin_filter import IsAdminFilter


def setup(dp: Dispatcher):
    logger.info("Setuping Filters...")
    event_handlers = [
        dp.message_handlers,
        dp.edited_message_handlers,
        dp.channel_post_handlers,
        dp.edited_channel_post_handlers,
    ]

    dp.filters_factory.bind(AuthRequired, event_handlers=event_handlers)
    dp.filters_factory.bind(IsAdminFilter, event_handlers=event_handlers)
