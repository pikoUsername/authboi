from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart, CommandHelp, Text, Command
from aiogram.types import ContentTypes

# handlers
from .help import bot_help, bot_about
from .start import register_user, log_in_user, back_to_main_menus
from .ref import get_refferals_bot
from .exit import remove_user, user_pass_verify, user_rm_accept
from .profile import get_user_profile
from .what_can import bot_what_can, back_to_reg_menu
from .name import start_change_name, wait_to_name_, accept_to_change_name
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
    bot_auth_password_verify,
    bot_start_auth,
)
from .email import accept_and_complete_emailcng, change_email_input, start_change_email
# end list of handlers

# states
from src.states.user import (
    ChangePassword,
    ChangeEmail,
    ChangeName,
    DescriptionChange,
    Exit,
    StartState
)


def setup(dp: Dispatcher):
    # just handlers with any state
    dp.register_message_handler(register_user, CommandStart(), state="*")
    dp.register_message_handler(bot_help, CommandHelp())
    dp.register_message_handler(start_change_name, Command(["change_name", "cng_name"]), state="*")
    dp.register_message_handler(wait_to_name_, state=ChangeName.wait_to_name)
    dp.register_message_handler(accept_to_change_name, state=ChangeName.wait_to_accept)
    dp.register_message_handler(get_refferals_bot, Command(commands=["ref", "referral"]), state="*")
    dp.register_message_handler(bot_about, Command("about"))
    dp.register_message_handler(bot_cancel_handler, Text("cancel", ignore_case=True), state="*")
    dp.register_message_handler(bot_cancel_handler, Command("cancel"), state="*")
    dp.register_message_handler(bot_auth_back, Command("back"), state="*")
    dp.register_message_handler(get_user_profile, Command("profile"), state="*")
    dp.register_message_handler(start_change_email, Command("change_email"), state="*")
    dp.register_message_handler(change_email_input, state=ChangeEmail.wait_to_email)
    dp.register_message_handler(accept_and_complete_emailcng, state=ChangeEmail.wait_to_accept)
    dp.register_message_handler(start_change_description, Command("change_desc"))
    dp.register_callback_query_handler(log_in_user, text="log_in", state="*")
    dp.register_message_handler(change_password, state=ChangePassword.wait_to_password)
    dp.register_message_handler(start_change_password,
                                Command(commands=["change_password", "cng_pass"]),
                                state="*")
    dp.register_callback_query_handler(back_to_main_menus, text="back_to_main_menu", state="*")
    dp.register_callback_query_handler(back_to_reg_menu, text="back_to_reg_menu")
    dp.register_callback_query_handler(bot_what_can, text="what_can")
    dp.register_message_handler(check_to_really_user, state=ChangePassword.wait_to_accept_with_password)
    dp.register_message_handler(changing_fully, state=ChangePassword.wait_to_accept_pass)
    dp.register_callback_query_handler(remove_user, text="admin_kb_delete_user")
    # handlers with states
    dp.register_message_handler(
        bot_auth_password_verify,
        state=StartState.wait_to_verify_pass,
        content_types=ContentTypes.TEXT,
    )
    dp.register_callback_query_handler(
        bot_start_auth,
        text="start_login",
        state="*",
    )
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
    dp.register_message_handler(
        remove_user,
        state="*",
    )
    dp.register_message_handler(
        user_pass_verify,
        state=Exit.wait_to_password,
        content_types=ContentTypes.TEXT,
    )
    dp.register_message_handler(
        user_rm_accept,
        state=Exit.wait_to_accept,
        content_types=ContentTypes.TEXT,
    )
