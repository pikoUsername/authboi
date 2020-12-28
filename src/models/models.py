from typing import List

from aiogram import types
from loguru import logger
from gino.schema import GinoSchemaVisitor
from gino import Gino
from sqlalchemy import sql

from src.config import POSTGRES_URI

db_ = Gino()


class User(db_.Model):
    __tablename__ = 'users'

    id = db_.Column(db_.Integer, db_.Sequence('user_id_seq'), primary_key=True)
    user_id = db_.Column(db_.BigInteger)
    username = db_.Column(db_.String(50))
    full_name = db_.Column(db_.String(100))
    login = db_.Column(db_.String(100))
    email = db_.Column(db_.String(200))
    password = db_.Column(db_.String(200))  # there must be hash
    referral = db_.Column(db_.Integer)
    description = db_.Column(db_.String)
    is_admin = db_.Column(db_.Boolean)

    query: sql.Select

    def __repr__(self):
        return f"<User(id='{self.id}', fullname='{self.full_name}', username='{self.username}')>"


class Event(db_.Model):
    __tablename__ = "Event"

    id = db_.Column(db_.BigInteger, primary_key=True, index=True)
    text = db_.Column(db_.String)
    link_img = db_.Column(db_.String(300))
    inline_text = db_.Column(db_.String)
    inline_btn_link = db_.Column(db_.String)


class DBCommands:
    async def get_user(self, user_id):
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user

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
            referral=None,
            login=None,
            email: str = None,
            password: str = None,
            is_admin: bool = False,
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
        new_user.is_admin = is_admin

        if referral:
            new_user.referral = int(referral)
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


async def create_db():
    await db_.set_bind(POSTGRES_URI)

    db_.gino: GinoSchemaVisitor
    await db_.gino.create_all()


async def close_db():
    bind = db_.pop_bind()
    if bind:
        logger.info("Closing DB...")
        await bind.close()
