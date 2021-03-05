from __future__ import annotations
from typing import List

from aiogram import types
from loguru import logger

from .user import User
from .event import Event
from iternal.config import ADMIN_IDS


class DBCommands:
    __slots__ = ()

    @staticmethod
    async def get_user(user_id: int) -> User:
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user

    @staticmethod
    async def remove_user(user_id: int) -> None:
        user = await User.query.where(User.user_id == user_id).gino.first()
        await user.delete()

    @staticmethod
    async def create_event(
        text: str,
        link: str,
        inline_text: str = None,
        inline_btn_link: str = None
    ) -> Event:
        new_event = Event()

        new_event.text = text
        new_event.link_img = link
        new_event.inline_text = inline_text
        new_event.inline_btn_link = inline_btn_link

        await new_event.create()
        return new_event

    @staticmethod
    async def get_all_users() -> List[User]:
        # todo optimaze this
        all_user = await User.query.gino.all()
        return all_user

    async def add_new_user(
        self,
        user: types.User,
        login: str,
        email: str,
        password: str = None,
    ) -> User:
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

    async def exit_user(self, user_id: int) -> None:
        import warnings

        warnings.warn("this Function is deprecated.")
        user = await self.get_user(user_id)
        user.is_authed = False
        await user.update().apply()

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
