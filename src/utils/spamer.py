import asyncio

from aiogram import types
from aiogram import exceptions
from loguru import logger as log

from src.loader import db, bot


async def send_message(chat_id: int, text: str, reply_markup: types.InlineKeyboardButton = None, photo: [types.InputFile, types.base.String] = None):
    try:
        if photo:
            await bot.send_photo(chat_id, text, reply_markup=reply_markup, photo=photo)
        else:
            await bot.send_message(chat_id, text, reply_markup=reply_markup)
    except exceptions.BotBlocked:
        log.error(f"Target [ID:{chat_id}]: blocked by user")
    except exceptions.ChatNotFound:
        log.error(f"Target [ID:{chat_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        log.error(f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(chat_id, text)  # Recursive call
    except exceptions.UserDeactivated:
        log.error(f"Target [ID:{chat_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        log.exception(f"Target [ID:{chat_id}]: failed")
    else:
        log.info(f"Target [ID:{chat_id}]: success")
        return True
    return False


async def send_to_all_users(text: str, img_link: str=None, inline_kb: types.InlineKeyboardMarkup=None):
    # TODO - make more beatiful and more better
    all_users = await db.get_all_users()

    if img_link:
        for user in all_users:
            await bot.send_photo(user.user_id, caption=text, reply_markup=inline_kb, photo=img_link)
    else:
        for user in all_users:
            await send_message(user.user_id, text=text)
