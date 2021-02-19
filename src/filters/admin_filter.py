from dataclasses import dataclass

from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data


@dataclass
class IsAdminFilter(BoundFilter):
    key = "is_admin"
    is_admin: bool

    async def check(self, _) -> bool:
        # get is_admin from user model
        return ctx_data.get()["user"].is_admin or False
