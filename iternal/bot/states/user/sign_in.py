from aiogram.dispatcher.filters.state import State, StatesGroup


class SignIn(StatesGroup):
    wait_login = State()
    wait_password = State()
