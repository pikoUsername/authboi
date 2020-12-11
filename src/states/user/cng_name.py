from aiogram.dispatcher.filters.state import StatesGroup, State

class ChangeName(StatesGroup):
    wait_to_name = State()
    wait_to_accept = State()