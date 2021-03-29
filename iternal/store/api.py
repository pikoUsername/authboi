from typing import List

from aiogram import types
from loguru import logger
from gino import GinoConnection

from .user import User
from .event import Event
from iternal.config import ADMIN_IDS
from iternal.utils.security import generate_hash

from .util import ContextGino


async def _get_user(_user_id: int) -> User:
    _user = await User.query.where(User.user_id == _user_id).gino.first()
    return _user


class DBCommands:
    __slots__ = "_current_user",

    async def get_user(self, user_id: int) -> User:
        user = getattr(self, '_current_user', None)
        # caches result to _current_user
        if user is None or user and user_id != user.user_id:
            user = await _get_user(user_id)
            setattr(self, '_current_user', user)
            return user

        if user is not None and user_id == user.user_id:
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
        **kwargs
    ) -> User:
        old_user = await self.get_user(user.id)

        if old_user:
            return old_user

        new_user = User()
        new_user.login = kwargs['login']
        new_user.email = kwargs['email']
        new_user.password = generate_hash(kwargs['password'])
        new_user.user_id = user.id
        new_user.username = user.username
        new_user.full_name = user.full_name

        new_user.is_admin = True if user.id in ADMIN_IDS else False

        await new_user.create()
        return new_user

    async def create_admin_user(self, user_id: int, remove: bool) -> int:
        user = await self.get_user(user_id)
        if user is None:
            raise ValueError("User is not registered in bot")

        await user.update(is_admin=not remove).apply()
        if remove:
            logger.warning("User {user} now IS NOT superuser", user=user_id)
        else:
            logger.warning("User {user} now IS superuser", user=user_id)
        # memory economy
        return 1

    async def acquire(self, *args, **kwargs) -> GinoConnection:
        """
        You must to close this, or later

        :return:
        """
        db_ = ContextGino.get_current()
        return db_.acquire(*args, **kwargs)
