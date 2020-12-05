from aiogram import types

from authboi.src.states.user.auth import StartState

async def bot_start(msg: types.Message):
    await msg.reply("Прежде чем пройти и использвать бота, авторизуйтесь!")

    StartState.wait_to_login.set()
    return await msg.answer("так что ввидите свои логин или имя!")






