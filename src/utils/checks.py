from aiogram import types

from ..loader import db


def is_admin(func):
    async def check(msg: types.Message):
        user = await db.get_user(msg.from_user.id)

        if user.is_admin:
            return True
        return False
    return check
