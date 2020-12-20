from aiogram import types
from aiogram.dispatcher.filters import Command

from src.loader import db, dp


@dp.message_handler(Command(["referral", "ref"]), state="*")
async def get_refferals_bot(msg: types.Message):
    user = await db.get_user(user_id=msg.from_user.id)

    if not user:
        return await msg.answer("Вы не авторизованы как пользветель!")

    check = await db.check_referrals()
    text = f"Вашы реффералы: \n{check}"
    await msg.answer(text)