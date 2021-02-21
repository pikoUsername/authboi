from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data


class AuthRequired(BoundFilter):
    key = "is_authed"

    def __init__(self, is_authed: bool):
        self.is_authed = is_authed

    async def check(self, _) -> bool:
        # get user if user is None then False, or True
        return bool(ctx_data.get()['user'])
