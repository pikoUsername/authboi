from typing import List

from aiogram import types
from loguru import logger

from .base import db_
from .user import User
from .event import Event
from ..config import ADMIN_IDS


class DBCommands:
    @staticmethod
    async def get_user(user_id: int) -> 'User':
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user

    async def remove_user(self, user_id: int) -> bool:
        user = await User.query.where(User.user_id == user_id).gino.first()

        if not user:
            logger.error("User doesnt exits")
            raise ValueError("User doesnt exits")
        await user.delete()
        return False


    async def create_event(self,
                           text: str,
                           link: str,
                           inline_text: str = None,
                           inline_btn_link:
                           str = None):
        new_event = Event()

        new_event.text = text
        new_event.link_img = link
        new_event.inline_text = inline_text
        new_event.inline_btn_link = inline_btn_link

        await new_event.create()
        return new_event

    async def add_new_user(
            self,
            user: types.User,
            login,
            email: str,
            password: str = None,
    ):
        old_user = await self.get_user(user.id)

        if old_user:
            return old_user

        new_user = User()
        new_user.login = login
        new_user.email = email
        new_user.password = password
        new_user.user_id = user.id
        new_user.username = user.username
        new_user.full_name = user.full_name
        if user.id in ADMIN_IDS:
            new_user.is_admin = True
        else:
            new_user.is_admin = False

        await new_user.create()
        return new_user

    async def count_users(self) -> int:
        total = await db_.func.count(User.id).gino.scalar()
        return total

    async def exit_user(self, user_id):
        user = await self.get_user(user_id)
        user.is_authed = False

    async def get_all_users(self) -> List:
        all_user = await db_.all(User.query)
        return all_user

    async def create_admin_user(self, user_id: int, remove):
        user = await self.get_user(user_id)
        if not user:
            logger.error("User is not registered in bot")
            raise ValueError("User is not registered in bot")

        logger.info(
            "Loaded user {user}.",
            user=user.user_id,
        )
        await user.update(is_admin=not remove).apply()
        if remove:
            logger.warning("User {user} now IS NOT superuser", user=user_id)
        else:
            logger.warning("User {user} now IS superuser", user=user_id)
        return True