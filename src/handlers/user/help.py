from aiogram import types

from src.utils.misc import rate_limit
from src.loader import db

@rate_limit(5, 'help')
async def bot_help(msg: types.Message):
    """
    getting tg_user and user by id,
    registered 42 line of __init__.py
    """
    user = await db.get_user(msg.from_user.id)

    if not user:
        text = [
            'Список команд: ',
            '/start - Начать диалог',
            '/help - Получить справку',
            '/cancel - отменяет вход',
            '/about - показывает гитхаб проекта',
            "/back - ход назад",
            "Если хотите полный список комманд, то вы должны пройти авторизацию, коммандой /start",
        ]
        return await msg.answer('\n'.join(text))
    text = [
        'Список команд: ',
        '/start - Начать диалог',
        '/help - Получить справку',
        '/cancel - отменяет вход',
        "/back - ход назад",
        '/about - показывает гитхаб бота',
        '/profile - Показывает ваш профиль',
        '/ref - Получить рефералку',
        '/change_password - Смена пароля',
        '/change_description - Смена описания',
        '/change_name - Смена Имени профиля',
        '/change_email - Смена Эмейла профиля'
    ]
    return await msg.answer("\n".join(text))


async def bot_about(msg: types.Message):
    await msg.answer("https://github.com/pikoUsername/authboi.git")
