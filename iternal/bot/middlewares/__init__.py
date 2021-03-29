from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.middlewares.environment import EnvironmentMiddleware
from loguru import logger

from .throttling import ThrottlingMiddleware
from .get_user import GetUser
from ..loader import db


def setup(dp: Dispatcher):
    logger.info("Setuping Middlewares...")

    dp.middleware.setup(GetUser())
    dp.middleware.setup(EnvironmentMiddleware(

    ))
    dp.middleware.setup(LoggingMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())
