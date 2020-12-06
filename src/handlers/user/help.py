from aiogram import types

from src.utils.misc import rate_limit


@rate_limit(5, 'help')
async def bot_help(msg: types.Message):
    text = [
        'Список команд: ',
        '/start - Начать диалог',
        '/help - Получить справку',
        '/cancel - отменяет вход',
        "/back - ход назад",
        "Если хотите полный список комманд, то вы должны пройти авторизацию, коммандой /start, или /login"
    ]
    await msg.answer('\n'.join(text))
