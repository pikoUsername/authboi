from aiogram.dispatcher.filters.state import StatesGroup, State


class DescriptionChange(StatesGroup):
    wait_to_description = State()
    wait_to_accept_change = State()