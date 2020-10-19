from aiogram.dispatcher.webhook import SendMessage
from aiogram.types import ContentType

from src.loader import dp
from src.states.level1.start import StartState

@dp.message_handler(state=StartState.wait_to_login, content_types=ContentType.TEXT)
async def