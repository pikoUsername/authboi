from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
from .get_user import GetUser


def setup(dp: Dispatcher):

    dp.middleware.setup(GetUser())
    dp.middleware.setup(ThrottlingMiddleware())
