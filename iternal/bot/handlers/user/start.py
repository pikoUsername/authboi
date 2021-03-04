from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.webhook import EditMessageText, SendMessage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loguru import logger

from iternal.bot.loader import dp
from iternal.bot.keyboards.inline.start import get_choice_kb
from iternal.store.user import User


@dp.message_handler(CommandStart())
async def register_user(msg: types.Message, user: User):
    # here check to user exists

    if user:
        return SendMessage(msg.chat.id, "Вы уже авторизованы как польветель!")

    logger.info(f"Start register_user handler user_id: {msg.from_user.id}, chat_id: {msg.chat.id}")
    return SendMessage(msg.chat.id, "Выбирите:", reply_markup=get_choice_kb())


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
                           reply_markup=get_choice_kb(),
                           message_id=call_back.message.message_id,
                           )
