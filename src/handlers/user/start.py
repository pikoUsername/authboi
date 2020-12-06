from aiogram import types
from loguru import logger

from src.states.user.auth import StartState
from src.loader import db

async def register_user(msg: types.Message):
    # here check to user exists
    tg_user = types.User.get_current()
    user = await db.get_user(tg_user.id)

    if user:
        return await msg.answer("Вы уже авторизованы как польветель! Если хотите выйти то комманда exit!")

    await msg.reply("Прежде чем пройти и использвать бота, авторизуйтесь! \n Предупреждение! Вы будете вышвернуты с аккаунта если будете уверены об этом пуоступке")

    await StartState.wait_to_login.set()
    return await msg.answer("так что ввидите свои логин или имя!")






