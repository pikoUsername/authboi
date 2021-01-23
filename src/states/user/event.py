from aiogram.dispatcher.filters.state import StatesGroup, State


class EventState(StatesGroup):
    wait_for_inline = State()
    wait_for_image = State()
    wait_for_text = State()
    wait_for_accept = State()
