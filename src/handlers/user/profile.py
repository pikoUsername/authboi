from aiogram import types

from src.loader import db

async def get_user_profile(msg: types.Message):
    tg_user = types.User.get_current()
    user = await db.get_user(tg_user.id)
    if user.is_authed is False and not user:
        return await msg.answer("Вы не авторизованы!")

    text = [
        f"Имя: {user.username}",
        f"Email: {user.email}",
        "пароль: не даем",
        f"Описание: {user.description}",
    ]

    return await msg.answer("\n".join(text))
