from aiogram import types

from src.keyboards.inline.start import choice_kb

async def bot_what_can(call_back: types.CallbackQuery):
    """
    used in - __init__.py
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

    return await call_back.message.edit_text('\n'.join(text), reply_markup=bot_desc_kb)


async def back_to_reg_menu(call_back: types.CallbackQuery):
    await call_back.message.edit_text("Выбирите: ", reply_markup=choice_kb)