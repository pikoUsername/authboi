def setup(dp: Dispatcher):
    # dp.register_callback_query_handler(get_statistic, text="admin_kb_get_statistic")
    # dp.register_callback_query_handler(get_users, text="admin_kb_get_all_users")
    # dp.register_callback_query_handler(from_all_users_back, text="back_from_all_users")
    # dp.register_callback_query_handler(again_to_admin_menu, text="again_admin")
    dp.register_message_handler(get_logs, Command("debug"), state="*")
    dp.register_message_handler(remove_logs, Command("remove_logs"), state="*")
    # dp.register_callback_query_handler(back_admin_kb, text='back_admin_kb')

from .debug import dp

__all__ = ["dp"]