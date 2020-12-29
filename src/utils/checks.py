from aiogram import types

from src.models.models import User

def is_admin(func):
    async def check(msg: types.Message):
        user = await User.query.where(User.user_id == msg.from_user.id).gino.first()

        if user.is_admin:
            return True
        return False
    return check
