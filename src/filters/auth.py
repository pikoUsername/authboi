from dataclasses import dataclass

from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data


@dataclass
class AuthRequired(BoundFilter):
    key = "is_authed"
    is_authed: bool

    async def check(self, obj) -> bool:
        data = ctx_data.get()
        user = data["user"]
        if user is None:
            return False
        return True

