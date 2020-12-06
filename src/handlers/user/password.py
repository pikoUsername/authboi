from typing import Optional

from aiogram import types

from src.loader import db
from src.states.user.cng_pass import ChangePassword

async def get_password(user_id: int) -> Optional[str, None]:
    user = await db.get_user(user_id)
    return user.password

async def start_change_password(msg: types.Message):
    tg_user = types.User.get_current()
    pass_ = await get_password(tg_user.id)

    if not pass_:
        return await msg.answer("Вы не авторизованы,\n из за этого вы не можете использвать эту комманду")

    await ChangePassword.wait_to_accept_pass.set()
    await msg.answer("Хорошо, Напишите ваш пароль для доказательства что это вы")

async def check_to_really_user(msg: types.Message):
    tg_user = types.User.get_current()
    pass_ = await get_password(tg_user.id)

    if pass_ != msg.text:
        return await msg.answer("Ваш пароль, не верный попробуйте еще разок.\n Может тогда получится")
    else:
        await ChangePassword.wait_to_password.set()
        await msg.answer("Теперь, напишите новый пароль на который вы хотите сменить:")

async def change_password(msg: types.Message):
    pass