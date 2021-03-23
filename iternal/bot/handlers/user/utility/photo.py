from io import BytesIO

from aiogram import types
from aiogram.types import ContentTypes

from iternal.bot.loader import dp


@dp.message_handler(commands='load_photo', content_types=ContentTypes.PHOTO)
async def bot_load_photo(m: types.Message):
    photo = m.photo[-1]
