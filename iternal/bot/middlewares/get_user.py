from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from ..loader import db


class GetUser(BaseMiddleware):
    async def get_user(self, data: dict, user: types.User):
        user = await db.get_user(user.id)

        data["user"] = user

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.get_user(data, message.from_user)

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
        await self.get_user(data, query.from_user)
