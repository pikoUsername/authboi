from aiogram.dispatcher.filters import BoundFilter

class UserFilter(BoundFilter):
    key = "is_user"
    is_user: bool = True

    async def check(self) -> bool:
        pass
