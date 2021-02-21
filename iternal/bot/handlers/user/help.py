from aiogram import types
from aiogram.dispatcher.filters import CommandHelp
from aiogram.dispatcher.handler import ctx_data
from aiogram.dispatcher.webhook import SendMessage

from iternal.bot.utils.throttling import rate_limit
from iternal.bot.loader import dp


@dp.message_handler(CommandHelp())
@rate_limit(5, "help")
async def bot_help(msg: types.Message):
    data = ctx_data.get()
    user = data['user']

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


@dp.message_handler(commands="about")
async def bot_about(msg: types.Message):
    return SendMessage(msg.chat.id, '<a href="https://github.com/pikoUsername/authboi.git)">github</a>')
