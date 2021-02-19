from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.exceptions import MessageIsTooLong
from aiogram.dispatcher.handler import ctx_data

from src.loader import dp
from src.utils.throttling import rate_limit


@dp.message_handler(Command("profile"), is_authed=True)
@rate_limit(5, 'profile')
async def get_user_profile(msg: types.Message):
    data = ctx_data.get()
    user = data["user"]
    text = [
        f"{user.description} - Описание",
        f"Имя: {user.username}",
        f"Email: {user.email}",
        "пароль: не даем",
    ]

    if user.is_admin:
        text.append("Вы Админ.")

    try:
        return SendMessage(msg.chat.id, "\n".join(text))
    except MessageIsTooLong:
        return SendMessage(msg.chat.id, "Сообщение слишком Длинное, измените описание своего профиля")
