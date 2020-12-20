from typing import List

from aiogram import types, Bot
from gino.schema import GinoSchemaVisitor
from gino import Gino
from sqlalchemy import sql

from data.config import POSTGRES_URI

db_ = Gino()

class User(db_.Model):
    __tablename__ = 'users'

    id = db_.Column(db_.Integer, db_.Sequence('user_id_seq'), primary_key=True)
    user_id = db_.Column(db_.BigInteger)
    username = db_.Column(db_.String(50))
    full_name = db_.Column(db_.String(100))
    login = db_.Column(db_.String(100))
    email = db_.Column(db_.String(200))
    password = db_.Column(db_.String(200)) # there must be hash
    referral = db_.Column(db_.Integer)
    description = db_.Column(db_.String)
    is_admin = db_.Column(db_.Boolean)

    query: sql.Select

    def __repr__(self):
        return f"<User(id='{self.id}', fullname='{self.full_name}', username='{self.username}')>"

class DBCommands:
    async def get_user(self, user_id):
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user

    async def add_new_user(
            self,
            referral=None,
            login=None,
            email: str=None,
            password: str=None,
            is_admin: bool=False,
    ):
        user = types.User.get_current()
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

    async def check_referrals(self):
        bot = Bot.get_current()
        user_id = types.User.get_current().id

        user = await User.query.where(User.user_id == user_id).gino.first()
        referrals = await User.query.where(User.referral == user.id).gino.all()

        return ", ".join([
            f"{num + 1}. " + (await bot.get_chat(referral.user_id)).get_mention(as_html=True)
            for num, referral in enumerate(referrals)
        ])

    async def exit_user(self, user_id):
        user = await self.get_user(user_id)
        user.is_authed = False

    async def get_all_users(self) -> List:
        user = await User.query.where().gino.all()
        return user

async def create_db(drop_after_restart: bool=True):
    await db_.set_bind(POSTGRES_URI)

    db_.gino: GinoSchemaVisitor
    if drop_after_restart:
        await db_.gino.drop_all()
    await db_.gino.create_all()