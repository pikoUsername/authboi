from aiogram import types
from aiogram.dispatcher.webhook import SendMessage

from iternal.bot.loader import dp
from iternal.bot.utils.embed import Embed


@dp.message_handler(commands="embed", is_authed=True, state="*")
async def bot_embed(m: types.Message):
    argv = m.get_args().split()

    [title, text] = [argv[0], argv[1]]

    e = Embed(title, text)

    return await m.answer(e.clean_embed)
