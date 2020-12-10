from aiogram import Dispatcher

from .admin import get_statistic, get_users, from_all_users_back

def setup(dp: Dispatcher):
    dp.register_callback_query_handler(get_statistic, text="admin_kb_get_statistic")
    dp.register_callback_query_handler(get_users, text="admin_kb_get_all_users")
    dp.register_callback_query_handler(from_all_users_back, text="back_from_all_users")