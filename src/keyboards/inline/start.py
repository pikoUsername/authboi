from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

choice_btns = [
    [
        InlineKeyboardButton("<< Что может этот бот", callback_data="what_can"),
        InlineKeyboardButton("Авторизоватся >>", callback_data="log_in"),
    ],
]

choice_kb = InlineKeyboardMarkup(inline_keyboard=choice_btns, row_width=1)