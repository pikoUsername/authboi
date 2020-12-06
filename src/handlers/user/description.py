from aiogram import types

from src.loader import db

async def change_description(msg: types.Message):
    tg_user = types.User.get_current()
    user = await db.get_user(tg_user.id)

    if not user:
        return await msg.answer("Вы не авторизованы как пользветель!")

    with