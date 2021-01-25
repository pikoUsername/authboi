from aiogram.dispatcher.filters.state import StatesGroup, State


class ChangeEmail(StatesGroup):
    wait_to_email = State()
    wait_to_accept = State()
