from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loguru import logger

from src.loader import db, dp
from src.keyboards.inline.start import choice_kb
from src.utils.throttling import rate_limit


@dp.message_handler(CommandStart())
@rate_limit(5, 'start')
async def register_user(msg: types.Message):
    # here check to user exists

    logger.info(f"Start register_user handler user_id: {msg.from_user.id}, chat_id: {msg.chat.id}")

    user = await db.get_user(msg.from_user.id)

    if user:
        return await msg.answer("Вы уже авторизованы как польветель!")

    return await msg.answer("Выбирите:", reply_markup=choice_kb)

@dp.callback_query_handler(text="log_in")
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

@dp.callback_query_handler(text="back_to_main_menu")
async def back_to_main_menus(call_back: types.CallbackQuery):
    await call_back.message.edit_text("Выбирите: ", reply_markup=choice_kb)



