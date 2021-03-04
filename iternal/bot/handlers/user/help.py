from aiogram import types
from aiogram.dispatcher.filters import CommandHelp
from aiogram.dispatcher.webhook import SendMessage

from iternal.bot.utils.throttling import rate_limit
from iternal.bot.loader import dp
from iternal.store.user import User
from iternal.bot.utils.embed import Embed
from iternal.bot.utils.html import a


@dp.message_handler(CommandHelp(), state="*")
@rate_limit(5, "help")
async def bot_help(msg: types.Message, user: User):
    if not user:
        text = [
            "Список команд: \n",
            "/start - Начать диалог.",
            "/help - Получить справку.",
            "/cancel - отменяет вход.",
            "/about - показывает гитхаб проекта.",
            "/back - ход назад.",
            "Если хотите полный список комманд, то вы должны пройти авторизацию, коммандой /start.",
        ]
        return SendMessage(msg.chat.id, "\n".join(text))
    text = [
        "Список команд: \n",
        "/start - Начать диалог.",
        "/help - Получить справку.",
        "/cancel - отменяет вход.",
        "/back - ход назад.",
        "/remove - удалить аккаунт.",
        "/about - показывает гитхаб бота.",
        "/profile - Показывает ваш профиль.",
        "/change_password - Смена пароля.",
        "/change_description - Смена описания.",
        "/change_name - Смена Имени профиля.",
        "/change_email - Смена Эмейла профиля."
    ]
    if user.is_admin:
        text += [
            "/logs - Показать все логи.\n"
            "/remove_all_logs - Удалить все логи.\n"
            "/start_event - Создать Ивент.\n"
            "/delete_user - Удалить Пользветеля.\n"
            "/set_admin - Улучшить Права Пользветеля.\n"
            "/start_event - Создать Ивент, или отпарвить всем сообщение.\n"
        ]

    return SendMessage(msg.chat.id, "\n".join(text))


@dp.message_handler(commands=("about", "faq"))
async def bot_about(msg: types.Message):
    e = Embed("FAQ")

    e.add_field("Исходники", a("Здесь", "https://github.com/pikoUsername"))
    e.add_field("Про что", "Этот бот создан для хранения текста, и прочих напминалок.")

    return SendMessage(msg.chat.id, e.clean_embed)
