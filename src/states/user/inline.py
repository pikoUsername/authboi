from aiogram.dispatcher.filters.state import StatesGroup, State

class InlineStates(StatesGroup):
    wait_for_inline_text = State()
    wait_for_reference =   State()
