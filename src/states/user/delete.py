from aiogram.dispatcher.filters.state import StatesGroup, State

class DeleteUserState(StatesGroup):
    wait_to_accept_delete  = State()
    wait_to_accept2_delete = State()