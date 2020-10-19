from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.webhook import SendMessage

from src.loader import dp
from src.states.level1.start import StartState

@dp.message_handler(CommandStart(), state="*")
async def cmd_start():
    SendMessage(
        '\n'
        'Hello i m bot for register and collect passwords and etc\n'
        'So get me your login.\n'
    )
    StartState.wait_to_login.set()





