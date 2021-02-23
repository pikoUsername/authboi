import asyncio
from typing import List

from aiogram import types
from aiogram import exceptions
from loguru import logger as log

from ..loader import db, bot
from iternal.store.user import User

_DEFAULT_IMG = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Flag_of_None.svg/1280px-Flag_of_None.svg.png"


async def send_message(chat_id: int,
                       *args, **message_params) -> bool:
    try:
        if 'photo' in message_params:
            await bot.send_photo(chat_id, *args, **message_params)
        else:
            await bot.send_message(chat_id, *args, **message_params)
    except exceptions.BotBlocked:
        log.error(f"Target [ID:{chat_id}]: blocked by user")
    except exceptions.ChatNotFound:
        log.error(f"Target [ID:{chat_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        log.error(f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(chat_id, *args, **message_params)  # Recursive call
    except exceptions.UserDeactivated:
        log.error(f"Target [ID:{chat_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        log.exception(f"Target [ID:{chat_id}]: failed")
    else:
        log.info(f"Target [ID:{chat_id}]: success")
        return True
    return False


async def send_to_given_users(user_ids: List[int], *args, **message_params):
    success = []
    unsuccessful = {}
    for user_id in user_ids:
        try:
            await bot.send_message(user_id, *args, disable_notification=True, **message_params)
            success.append(user_id)
        except exceptions.TelegramAPIError as e:
            unsuccessful[user_id] = str(e)

    if unsuccessful:
        fmt = []
        for key, value in unsuccessful.items():
            error = f"{key} - {value}"
            fmt.append(error)
            return fmt
    return success


async def notify_all_admins(*args, **message_params):
    admins = await User.query.where(User.is_admin is True).gino.all()
    admin_ids = []
    for admin in admins:
        admin_ids.append(admin.user_id)

    result = await send_to_given_users(admin_ids, *args, **message_params)  # MAYBE shity code but idk
    return result


async def send_to_all_users(
    text: str,
    img_link: str = None,
    inline_kb: types.InlineKeyboardMarkup = None
):
    all_users = await db.get_all_users()

    for user in all_users:
        # DEFAULT_IMG using, bc telegram wont to see that
        await send_message(user.user_id, photo=img_link or _DEFAULT_IMG, caption=text, reply_markup=inline_kb)
