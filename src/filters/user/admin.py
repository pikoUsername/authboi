from aiogram.dispatcher.filters import BoundFilter

class AdminFilter(BoundFilter):
    key = 'is_admin'
    is_admin: bool = False


