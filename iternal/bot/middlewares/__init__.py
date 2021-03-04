from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from loguru import logger

from .throttling import ThrottlingMiddleware
from .get_user import GetUser


def setup(dp: Dispatcher):
    logger.info("Setuping Middlewares...")

    dp.middleware.setup(GetUser())
    dp.middleware.setup(LoggingMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())
