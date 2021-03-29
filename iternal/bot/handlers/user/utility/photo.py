from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes

from iternal.bot.loader import dp
from iternal.store.photo import Photo


@dp.message_handler(commands='load_photo', content_types=ContentTypes.PHOTO)
async def bot_load_photo(m: types.Message, state: FSMContext):
    url: str = await m.photo[-1].get_url()

