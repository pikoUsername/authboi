from aiogram.dispatcher.filters.state import StatesGroup, State

class SignIn(StatesGroup):
    wait_to_type_login = State()
    wait_to_type_password = State()