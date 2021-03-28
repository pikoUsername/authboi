from aiogram import types
from aiogram.types import ContentTypes

from iternal.bot.loader import dp
from iternal.store.photo import Photo


@dp.message_handler(commands='load_photo', content_types=ContentTypes.PHOTO)
async def bot_load_photo(m: types.Message, state: FSM):
    photo = m.photo[-1]
    url: str = await photo.get_url()
