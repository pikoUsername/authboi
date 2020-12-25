from aiogram import types

from src.loader import db, bot

async def send_to_all_users(text: str, img_link: str=None, inline_kb: types.InlineKeyboardMarkup=None):
    # TODO - make more beatiful and more better
    all_users = await db.get_all_users()

    try:
        if img_link:
            for user in all_users:
                await bot.send_photo(user.user_id, caption=text, reply_markup=inline_kb)
        else:
            for user in all_users:
                await bot.send_message(user.user_id, text=text)
    except Exception as e:
        raise e

