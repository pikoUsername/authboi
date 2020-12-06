from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart, CommandHelp, Text, Command
from aiogram.types import ContentTypes

from .help import bot_help
from .start import register_user
from .ref import get_refferals_bot
from .exit import remove_user, user_exit
from .auth import (
    bot_auth_login,
    bot_cancel_handler,
    bot_auth_password,
    bot_auth_accept,
    bot_auth_back,
    bot_auth_email,
)

from src.states.user.auth import StartState

def setup(dp: Dispatcher):
    dp.register_message_handler(register_user, CommandStart(), state="*")
    dp.register_message_handler(bot_help, CommandHelp(), state="*")
    dp.register_message_handler(bot_cancel_handler, Text("cancel", ignore_case=True), state="*")
    dp.register_message_handler(bot_cancel_handler, Command("cancel"), state="*")
    dp.register_message_handler(bot_auth_back, Command("back"), state="*")
    dp.register_message_handler(
        bot_auth_login,
        state=StartState.wait_to_login,
        content_types=ContentTypes.TEXT,
    )
    dp.register_message_handler(
        bot_auth_password,
        state=StartState.wait_to_password,
        content_types=ContentTypes.TEXT,
    )
    dp.register_message_handler(
        bot_auth_accept,
        state=StartState.wait_to_accept,
        content_types=ContentTypes.TEXT,
    )
    dp.register_message_handler(
        bot_auth_email,
        state=StartState.wait_to_email,
        content_types=ContentTypes.TEXT,
    )
