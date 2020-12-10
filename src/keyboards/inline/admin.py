from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_btns = [
    [
        InlineKeyboardButton("Пользветели", callback_data="admin_kb_get_all_users"),
        InlineKeyboardButton("Статистка", callback_data="admin_kb_get_statistic"),
        InlineKeyboardButton("<< Назад", callback_data="")
    ]
]

admin_kb = InlineKeyboardMarkup(inline_keyboard=admin_btns, row_width=2)