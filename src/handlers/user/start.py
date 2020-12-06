from aiogram import types

from src.states.user.auth import StartState
from src.loader import db

async def register_user(msg: types.Message, user: types.User):
    # here check to user exists
    old_user = db.get_user(user.id)
    if old_user:
        return await msg.answer("Вы уже авторизованы как пользветель! Вы можете выйти из система коммандой /exit")
    referral = msg.get_args()

    await db.add_new_user(referral=referral)
    await msg.reply("Прежде чем пройти и использвать бота, авторизуйтесь!")

    await StartState.wait_to_login.set()
    return await msg.answer("так что ввидите свои логин или имя!")






