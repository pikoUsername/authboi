from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.webhook import SendMessage

from iternal.bot.loader import dp
from iternal.store.user import User
from iternal.bot.utils.misc import fill_auth_final


@dp.message_handler(Command("profile"), is_authed=True)
async def get_user_profile(msg: types.Message, user: User):
    e = fill_auth_final(user.password, user.login, user.email)

    return SendMessage(msg.chat.id, e)
