from aiogram import types

from src.models.models import DBCommands

db = DBCommands()

async def make_user_profile(user_id: int) -> str:
    user = await db.get_user(user_id)
    text = [
        f"Имя: {user.name}",
        f"Email: {user.email}",
        "пароль: не даем",
        f"Описание: {user.description}" if user.description else "Описание: Нету",
    ]
    return "\n".join(text)


async def get_user_profile(msg: types.Message):
    tg_user = types.User.get_current()
    user_profile = await make_user_profile(tg_user.id)

    return await msg.answer(user_profile)
