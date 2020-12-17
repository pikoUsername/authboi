from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,
from aiogram.utils.callback_data import CallbackData
from aiogram import types

class PaginatorSession:
    def __init__(self, text: str, message: types.Message):
        self.msg = message
        self.text = text
        self.current_page = 0
        self.pages = []
        self.call_back_data = CallbackData("num_page")
        self.keyboard = []

    async def separator(self): pass #TODO separator for text if text more than 2000 function separate this until end

    async def get_new_page(self): pass #TODO get new page base on current page

    async def create_keyboard(self): pass #TODO create keyboard

    async def send_paged_message(self): pass #TODO send all data by peace
