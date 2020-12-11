from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loguru import logger

from src.states.user.auth import StartState
from src.loader import db
from src.keyboards.inline.start import choice_kb
# from src.keyboards.inline.admin import admin_kb
# from data.config import ADMIN_IDS
from src.utils.misc.throttling import rate_limit

@rate_limit(5, 'start')
async def register_user(msg: types.Message):
    # here check to user exists

    logger.info(f"Start register_user handler user_id: {msg.from_user.id}, chat_id: {msg.chat.id}")
    #if msg.from_user.id in ADMIN_IDS:
    #    logger.info('Admin logged in!')
    #    await msg.answer(
    #        "Вы авторизованы как админ, админ панель:",
    #        reply_markup=admin_kb,
    #    )
    #    return

    tg_user = types.User.get_current()
    user = await db.get_user(tg_user.id)

    if user and user.is_authed is True:
        return await msg.answer("Вы уже авторизованы как польветель!")

    return await msg.answer("Выбирите:", reply_markup=choice_kb)


async def log_in_user(call_back: types.CallbackQuery):
    back_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton("<< Назад", callback_data="back_to_main_menu"),
            InlineKeyboardButton("Начать >>", callback_data="start_login"),
        ],
    ])

    try:
        await call_back.message.edit_text("Прежде чем пройти и использвать бота, авторизуйтесь! видите Логин или Имя", reply_markup=back_kb)
    except Exception as e:
        logger.exception(f"Here exception 45-line, {e}")


async def back_to_main_menus(call_back: types.CallbackQuery):
    await call_back.message.edit_text("Выбирите: ", reply_markup=choice_kb)



