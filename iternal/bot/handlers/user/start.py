from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.handler import ctx_data
from aiogram.dispatcher.webhook import EditMessageText, SendMessage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loguru import logger

from src.loader import dp
from src.keyboards.inline.start import choice_kb


@dp.message_handler(CommandStart())
async def register_user(msg: types.Message):
    # here check to user exists
    user = ctx_data.get()['user']

    if user:
        return await msg.answer("Вы уже авторизованы как польветель!")

    logger.info(f"Start register_user handler user_id: {msg.from_user.id}, chat_id: {msg.chat.id}")
    return SendMessage(msg.chat.id, "Выбирите:", reply_markup=choice_kb)


@dp.callback_query_handler(text="log_in")
async def log_in_user(call_back: types.CallbackQuery):
    back_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton("<< Назад", callback_data="back_to_main_menu"),
            InlineKeyboardButton("Начать >>", callback_data="start_login"),
        ],
    ])
    return EditMessageText(chat_id=call_back.message.chat.id,
                           message_id=call_back.message.message_id,
                           text="Прежде чем пройти и использвать бота, авторизуйтесь! видите Логин или Имя.",
                           reply_markup=back_kb
                           )


@dp.callback_query_handler(text="back_to_main_menu")
async def back_to_main_menus(call_back: types.CallbackQuery):
    return EditMessageText(chat_id=call_back.message.chat.id,
                           text="Меню: ",
                           reply_markup=choice_kb,
                           message_id=call_back.message.message_id,
                           )
