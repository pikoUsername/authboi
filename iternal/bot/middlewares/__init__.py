from aiogram import Dispatcher
from loguru import logger

from .throttling import ThrottlingMiddleware
from .get_user import GetUser


def setup(dp: Dispatcher):
    logger.info("Setuping Middlewares...")

    dp.middleware.setup(GetUser())
    dp.middleware.setup(ThrottlingMiddleware())
