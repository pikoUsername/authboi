from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart, CommandHelp, Text, Command
from aiogram.types import ContentTypes

# handlers
from .help import bot_help, bot_about
from .start import register_user, sign_in_user, log_in_user
from .ref import get_refferals_bot
from .exit import remove_user, user_exit
from .profile import get_user_profile
from .password import (
    start_change_password,
    change_password,
    changing_fully,
    check_to_really_user
)
from .description import (
    change_description,
    start_change_description,
    accept_change_description,
)
from .auth import (
    bot_auth_login,
    bot_cancel_handler,
    bot_auth_password,
    bot_auth_accept,
    bot_auth_back,
    bot_auth_email,
)
from .signup import start_sign_in, login_sign_in, password_sign_in
# end list of handlers

# states
from src.states.user.desc import DescriptionChange
from src.states.user.auth import StartState
from src.states.user.cng_pass import ChangePassword
from src.states.user.sign_up import SignIn

def setup(dp: Dispatcher):
    # just handlers with any state
    dp.register_message_handler(register_user, CommandStart(), state="*")
    dp.register_message_handler(bot_help, CommandHelp())
    dp.register_message_handler(bot_about, Command("about"))
    dp.register_message_handler(bot_cancel_handler, Text("cancel", ignore_case=True), state="*")
    dp.register_message_handler(bot_cancel_handler, Command("cancel"), state="*")
    dp.register_message_handler(bot_auth_back, Command("back"), state="*")
    dp.register_message_handler(get_user_profile, Command("profile"), state="*")
    dp.register_message_handler(start_change_description, Command("change_desc"))
    dp.register_callback_query_handler(sign_in_user, text="sign_in", state="*")
    dp.register_callback_query_handler(log_in_user, text="log_in", state="*")
    dp.register_message_handler(change_password, state=ChangePassword.wait_to_password)
    dp.register_message_handler(start_change_password,
                                Command(commands=["change_password", "cng_pass"]),
                                state="*")
    dp.register_message_handler(login_sign_in, state=SignIn.wait_to_type_login)
    dp.register_message_handler(password_sign_in, state=SignIn.wait_to_type_password)
    dp.register_message_handler(check_to_really_user, state=ChangePassword.wait_to_accept_with_password)
    dp.register_message_handler(changing_fully, state=ChangePassword.wait_to_accept_pass)

    # handlers with states
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
    dp.register_message_handler(
        change_description,
        state=DescriptionChange.wait_to_description,
        content_types=ContentTypes.TEXT,
    )
    dp.register_message_handler(
        accept_change_description,
        state=DescriptionChange.wait_to_accept_change,
        content_types=ContentTypes.TEXT,
    )
