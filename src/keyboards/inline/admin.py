from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_btns = [
    [
        InlineKeyboardButton("Пользветели", callback_data="admin_kb_get_all_users"),
        InlineKeyboardButton("Статистка", callback_data="admin_kb_get_statistic"),
        InlineKeyboardButton("Удалить Пользветеля", callback_data="admin_kb_delete_user"),
    ]
]

admin_kb = InlineKeyboardMarkup(inline_keyboard=admin_btns, row_width=2)