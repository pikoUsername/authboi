from aiogram import types

from src.loader import db
from src.utils.throttling import rate_limit

@rate_limit(5, 'profile')
async def get_user_profile(msg: types.Message):
    user = await db.get_user(msg.from_user.id)

    if not user:
        return await msg.answer("Вы не авторизованы!")

    text = [
        f"Имя: {user.username}",
        f"Email: {user.email}",
        "пароль: не даем",
        f"Описание: {user.description}",
    ]

    return await msg.answer("\n".join(text))
