from aiogram import Dispatcher
from loguru import logger

# copy from aiogram bot there is it (https://github.com/aiogram/bot/blob/master/app/filters/__init__.py) hm..
def setup(dispatcher: Dispatcher):
    logger.info("Configure filters...")
    from .user import Is_private
    from .admin import AdminFilter

    text_messages = [
        dispatcher.message_handlers,
        dispatcher.edited_message_handlers,
        dispatcher.channel_post_handlers,
        dispatcher.edited_channel_post_handlers,
    ]

    dispatcher.filters_factory.bind(Is_private, event_handlers=text_messages)
    dispatcher.filters_factory.bind(AdminFilter, event_handlers=text_messages)
