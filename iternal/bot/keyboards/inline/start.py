from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_choice_kb():
    choice_btns = [
        [
            InlineKeyboardButton("<< Что может этот бот", callback_data="what_can"),
            InlineKeyboardButton("Авторизоватся >>", callback_data="log_in"),
            InlineKeyboardButton("Войти <>", callback_data="sign_in")
        ],
    ]

    choice_kb = InlineKeyboardMarkup(inline_keyboard=choice_btns, row_width=1)
    return choice_kb
