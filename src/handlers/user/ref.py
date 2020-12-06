from aiogram import types

from src.models.models import DBCommands

db = DBCommands()

async def get_refferals_bot(msg: types.Message, user: types.User):
    user = await db.get_user(user_id=user.id)
    if not user.is_authed:
        return await msg.answer("Вы не авторизованы как пользветель!")
    check = await db.check_referrals()
    text = f"Вашы реффералы: \n{check}"
    await msg.answer(text)