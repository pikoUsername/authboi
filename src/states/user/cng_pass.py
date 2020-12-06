from aiogram.dispatcher.filters.state import StatesGroup, State

class ChangePassword(StatesGroup):
    wait_to_accept_with_password = State()
    wait_to_password             = State()
    wait_to_accept_pass          = State()