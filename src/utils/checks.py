from aiogram import types
from loguru import logger

from ..loader import db


def is_admin(func):  # idk why not working
    async def check(msg: types.Message):
        user = await db.get_user(msg.from_user.id)

        if user.is_admin:
            return True
        return False
    return check


async def check_for_admin(msg: types.Message, user_id: int):
    user = await db.get_user(user_id)

    if not user:
        return await msg.reply("Пользветель Не найден")
    elif not user.is_admin:
        return await msg.reply("Пользветель Не Админ")
    return True
