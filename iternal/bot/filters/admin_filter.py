from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data


class IsAdminFilter(BoundFilter):
    key = "is_admin"

    def __init__(self, is_admin: bool):
        self.is_admin = is_admin

    async def check(self, *_) -> bool:
        del _
        # get is_admin from user model
        user = ctx_data.get()["user"]

        try:
            return user.is_admin
        except AttributeError:
            pass
        finally:
            return False