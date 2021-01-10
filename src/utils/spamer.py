import asyncio
from typing import List, Tuple, Dict

from aiogram import types
from aiogram import exceptions
from loguru import logger as log

from src.loader import db, bot
from src.models.user import User


async def send_message(chat_id: int,
                       *args, **message_params) -> bool:
    try:
        if message_params.get('photo'):
            await bot.send_photo(chat_id, *args, **message_params)
        else:
            await bot.send_message(chat_id,  *args, **message_params)
    except exceptions.BotBlocked as e:
        log.error(f"Target [ID:{chat_id}]: blocked by user")
    except exceptions.ChatNotFound as e:
        log.error(f"Target [ID:{chat_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        log.error(f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(chat_id, *args, **message_params)  # Recursive call
    except exceptions.UserDeactivated as e:
        log.error(f"Target [ID:{chat_id}]: user is deactivated")
    except exceptions.TelegramAPIError as e:
        log.exception(f"Target [ID:{chat_id}]: failed")
    else:
        log.info(f"Target [ID:{chat_id}]: success")
        return True
    return False


async def send_to_given_users(user_ids: List[int], *args, **message_params):
    success = ['Успешно']
    unsuccessful = {}
    for user_id in user_ids:
        try:
            await bot.send_message(user_id, *args, disable_notification=True, **message_params)
            success.append(user_id)
        except exceptions.TelegramAPIError as e:
            unsuccessful[user_id] = str(e)

    if unsuccessful:
        fmt = ["Здесь Немного Ошибок, Чуточку"]
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
    print(admin_ids)
    result = await send_to_given_users(admin_ids, *args, **message_params)  # MAYBE shity code but idk
    return result


async def send_to_all_users(text: str, img_link: str = None, inline_kb: types.InlineKeyboardMarkup = None):
    # TODO - make more beatyful and more better
    all_users = await db.get_all_users()

    if img_link:
        for user in all_users:
            await bot.send_photo(user.user_id, caption=text, reply_markup=inline_kb, photo=img_link)
    else:
        for user in all_users:
            await send_message(user.user_id, text=text)
