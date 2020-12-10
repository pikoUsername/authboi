from aiogram.dispatcher.filters.state import State, StatesGroup

class StartState(StatesGroup):
    wait_to_login    = State()
    wait_to_email    = State()
    wait_to_password = State()
    wait_to_verify_pass = State()
    wait_to_accept   = State()