from aiogram import types
from loguru import logger

from src.states.user.auth import StartState
from src.loader import db
from src.keyboards.inline.start import choice_kb
from src.keyboards.inline.admin import admin_kb
from data.config import ADMIN_IDS


async def register_user(msg: types.Message):
    # here check to user exists

    logger.info(f"Start register_user handler user_id: {msg.from_user.id}, chat_id: {msg.chat.id}")
    if msg.chat.id in ADMIN_IDS:
        await msg.delete_reply_markup()
        return await msg.answer(
            "Вы авторизованы как админ, админ панель:",
            reply_markup=admin_kb,
        )

    tg_user = types.User.get_current()
    user = await db.get_user(tg_user.id)

    if user and user.is_authed is True:
        return await msg.answer("Вы уже авторизованы как польветель!")

    return await msg.answer("Выбирите:", reply_markup=choice_kb)


async def log_in_user(call_back: types.CallbackQuery):
    await StartState.wait_to_login.set()

    await call_back.message.answer("Прежде чем пройти и использвать бота, авторизуйтесь! \n видите Логин или Имя")





