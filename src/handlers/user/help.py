from aiogram import types
from aiogram.dispatcher.filters import CommandHelp
from aiogram.dispatcher.webhook import SendMessage

from src.utils.throttling import rate_limit
from src.loader import db, dp, bot


@dp.message_handler(CommandHelp())
@rate_limit(5, "help")
async def bot_help(msg: types.Message):
    """
    getting tg_user and user by id,
    registered 42 line of __init__.py
    """
    user = await db.get_user(msg.from_user.id)

    if not user:
        text = [
            "Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку",
            "/cancel - отменяет вход",
            "/about - показывает гитхаб проекта",
            "/back - ход назад",
            "Если хотите полный список комманд, то вы должны пройти авторизацию, коммандой /start",
        ]
        return await msg.answer(text="\n".join(text))
    text = (
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
        "/change_email - Смена Эмейла профиля.",
        "/logs - Показать все логи(Админ).",
        "/remove_all_logs - Удалить все логи(Админ).",
        "/start_event - Создать Ивент.",
        "/delete_user - Удалить Пользветеля",
    )

    return await bot.send_message(chat_id=msg.chat.id, text="\n".join(str(v) for v in text))


@dp.message_handler(commands="about")
async def bot_about(msg: types.Message):
    return SendMessage(chat_id=msg.chat.id, text="(https://github.com/pikoUsername/authboi.git)")
