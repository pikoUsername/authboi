from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

choice_btns = [
    [
        InlineKeyboardButton("Авторизоваться", callback_data="log_in"),
        InlineKeyboardButton("Войти", callback_data="sign_in"),
    ],
]

choice_kb = InlineKeyboardMarkup(inline_keyboard=choice_btns, row_width=1)