from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from aiogram.types import ChatType


class Is_private(BoundFilter):
    key = 'is_private'

    is_private: bool

    def check(self) -> bool:
        return ChatType.is_private()