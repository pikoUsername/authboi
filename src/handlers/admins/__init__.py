from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command

# from .admin import get_statistic, get_users, from_all_users_back, back_admin_kb, again_to_admin_menu
from .debug import get_logs, remove_logs

def setup(dp: Dispatcher):
    # dp.register_callback_query_handler(get_statistic, text="admin_kb_get_statistic")
    # dp.register_callback_query_handler(get_users, text="admin_kb_get_all_users")
    # dp.register_callback_query_handler(from_all_users_back, text="back_from_all_users")
    # dp.register_callback_query_handler(again_to_admin_menu, text="again_admin")
    dp.register_message_handler(get_logs, Command("debug"))
    dp.register_message_handler(remove_logs, Command("remove_logs"))
    # dp.register_callback_query_handler(back_admin_kb, text='back_admin_kb')
