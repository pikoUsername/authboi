from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from data.config import ADMIN_IDS

class AdminFilter(BoundFilter):
    key = 'is_admin'

    is_admin: bool

    async def check(self, message: Message) -> bool:
        return message.from_user.id in ADMIN_IDS
