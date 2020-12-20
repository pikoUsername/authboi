from aiogram import types
from aiogram.utils.exceptions import MessageIsTooLong

from src.loader import db, dp
from src.utils.throttling import rate_limit

@rate_limit(5, 'profile')
async def get_user_profile(msg: types.Message):
    user = await db.get_user(msg.from_user.id)

    if not user:
        return await msg.answer("Вы не авторизованы!")

    text = [
        f"{user.description} - Описание",
        f"Имя: {user.username}",
        f"Email: {user.email}",
        "пароль: не даем",
    ]

    try:
        return await msg.answer("\n".join(text))
    except MessageIsTooLong:
        await msg.answer("Сообщение слишком Длинное, измените описание своего профиля")