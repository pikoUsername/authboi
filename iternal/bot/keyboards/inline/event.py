from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_event_kb():
    inline_choice_btns = [
        [
            InlineKeyboardButton(text="Да", callback_data="admin_event_inline_choice_yes"),
            InlineKeyboardButton(text="Нет", callback_data="admin_event_inline_choice_no"),
        ]
    ]

    inline_choice_event = InlineKeyboardMarkup(inline_keyboard=inline_choice_btns, row_width=2)
    return inline_choice_event
