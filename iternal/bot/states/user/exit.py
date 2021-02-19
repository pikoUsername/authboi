from aiogram.dispatcher.filters.state import StatesGroup, State


class Exit(StatesGroup):
    wait_to_password = State()
    wait_to_accept = State()
