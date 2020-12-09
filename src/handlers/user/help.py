from aiogram import types

from src.utils.misc import rate_limit
from src.loader import db

@rate_limit(5, 'help')
async def bot_help(msg: types.Message):
    tg_user = types.User.get_current()
    user = await db.get_user(tg_user.id)

    if not user:
        text = [
            'Список команд: ',
            '/start - Начать диалог',
            '/help - Получить справку',
            '/cancel - отменяет вход',
            '/about - показывает гитхаб проекта',
            "/back - ход назад",
            "Если хотите полный список комманд, то вы должны пройти авторизацию, коммандой /start, или /login"
        ]
        return await msg.answer('\n'.join(text))
    text = [
        'Список команд: ',
        '/start - Начать диалог',
        '/help - Получить справку',
        '/cancel - отменяет вход',
        "/back - ход назад",
        '/about - показывает гитхаб бота',
        '/change_password - Смена пароля',
        '/profile - Показывает ваш профиль',
        '/change_description - Смена описания',
        '/ref - Получить рефералку'
    ]
    return await msg.answer("\n".join(text))


async def bot_about(msg: types.Message):
    await msg.answer("https://github.com/pikoUsername/authboi.git")
