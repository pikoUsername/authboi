from aiogram import types
from aiogram.dispatcher.webhook import EditMessageText

from src.loader import dp
from src.keyboards.inline.start import choice_kb


@dp.callback_query_handler(text="what_can", state="*")
async def bot_what_can(call_back: types.CallbackQuery):
    """
    CallbackData - back_to_reg_menu
    InlineButtons - << Back <<
    """
    text = [
        "Описание: ",
        "Этот бот с помощью комманды /text Может записывать что вы ввели в эту комманду.",
        "Затем вы можете Вывести все это с помощью /all",
        "И у этого бота есть авторизация!"
    ]
    bot_desc = [
        [
            types.InlineKeyboardButton("<< Назад <<", callback_data="back_to_reg_menu")
        ]
    ]
    bot_desc_kb = types.InlineKeyboardMarkup(inline_keyboard=bot_desc)

    return EditMessageText('\n'.join(text), call_back.message.chat.id,
                           reply_markup=bot_desc_kb, message_id=call_back.message.message_id)


@dp.callback_query_handler(text="back_to_reg_menu", state="*")
async def back_to_reg_menu(call_back: types.CallbackQuery):
    return EditMessageText("Выбирите: ", call_back.message.chat.id,
                           message_id=call_back.message.message_id, reply_markup=choice_kb)