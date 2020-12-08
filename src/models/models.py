from aiogram import types, Bot
from gino.schema import GinoSchemaVisitor
from gino import Gino
from sqlalchemy import (
    Column,
    Integer,
    Sequence,
    String,
    BigInteger,
    Boolean,
)
from sqlalchemy import sql

from data.config import POSTGRES_URI

db = Gino()

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    user_id = Column(BigInteger)
    username = Column(String(50))
    full_name = Column(String(100))
    login = Column(String(100))
    email = Column(String(200))
    password = Column(String(200)) # there must be hash
    referal = Column(Integer)
    is_authed = Column(Boolean)
    is_password_changed = Column(Boolean)
    description = Column(String(250))
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
            is_authed: bool=False
    ):
        user = types.User.get_current()
        old_user = await self.get_user(user.id)

        if old_user:
            return old_user

        new_user = User()
        new_user.login = login
        new_user.is_authed = is_authed
        new_user.email = email
        new_user.password = password
        new_user.user_id = user.id
        new_user.username = user.username
        new_user.full_name = user.full_name

        if referral:
            new_user.referral = int(referral)
        await new_user.create()
        return new_user

    async def get_user_by_login(self, login):
        user = await User.query.where(User.login == login).gino.first()
        return user

    async def get_user_by_password(self, password):
        user = await User.query.where(User.password == password).gino.first()
        return user

    async def sign_in(self, login):
        user = await User.query.where(User.login == login).gino.first()

        if user is None or user.is_authed is True:
            return

        return user


    async def count_users(self) -> int:
        total = await db.func.count(User.id).gino.scalar()
        return total

    async def check_for_authed(self, user_id):
        tg_user = types.User.get_current()
        user = await self.get_user(user_id)

    async def check_referrals(self):
        bot = Bot.get_current()
        user_id = types.User.get_current().id

        user = await User.query.where(User.user_id == user_id).gino.first()
        referrals = await User.query.where(User.referral == user.id).gino.all()

        return ", ".join([
            f"{num + 1}. " + (await bot.get_chat(referral.user_id)).get_mention(as_html=True)
            for num, referral in enumerate(referrals)
        ])

    async def remove_user(self, user_id):
        user = await self.get_user(user_id)
        user.__tablename__.drop()

    async def exit_user(self, user_id):
        user = await self.get_user(user_id)
        user.is_authed = False

async def create_db():
    await db.set_bind(POSTGRES_URI)

    db.gino: GinoSchemaVisitor
    await db.gino.drop_all()
    await db.gino.create_all()