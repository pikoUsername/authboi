from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.exceptions import MessageIsTooLong

from iternal.bot.utils.embed import Embed
from iternal.bot.loader import dp
from iternal.store.user import User


@dp.message_handler(Command("profile"), is_authed=True)
async def get_user_profile(msg: types.Message, user: User):
    e = Embed("Профиль")

    e.add_field("Имя", user.username)
    e.add_field("Описание", user.description or "Без Описания")
    e.add_field("Email", user.email)
    e.add_field("Пароль", "nope")

    try:
        return SendMessage(msg.chat.id, e.clean_embed)
    except MessageIsTooLong:
        return SendMessage(msg.chat.id, "Сообщение слишком Длинное, измените описание своего профиля")
