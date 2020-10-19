from aiogram.dispatcher.filters.state import State, StatesGroup

class StartState(StatesGroup):
    wait_to_login = State()
    wait_to_password = State()


