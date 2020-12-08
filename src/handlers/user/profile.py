from aiogram import types
from aiogram.dispatcher import FSMContext

from src.loader import db

async def get_user_profile(msg: types.Message, state: FSMContext):
    tg_user = types.User.get_current()
    user = await db.get_user(tg_user.id)
    if user is None:
        return await msg.answer("Вы не авторизованы!")

    text = [
        f"Имя: {user.username}",
        f"Email: {user.email}",
        "пароль: не даем",
        f"Описание: {user.description}",
    ]

    return await msg.answer("\n".join(text))
