from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

auth_btns = [
    [
        InlineKeyboardButton("Войти", callback_data="sign_up_auth"),
        InlineKeyboardButton("Регистрация", callback_data="sign_in_auth")
    ],
]