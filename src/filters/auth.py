from dataclasses import dataclass

from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data


@dataclass
class AuthRequired(BoundFilter):
    key = "is_authed"
    is_authed: bool

    async def check(self, _) -> bool:
        # get user if user is None then False, or True
        return bool(ctx_data.get()['user'])
