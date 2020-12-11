from aiogram import types
from loguru import logger

from src.states.user.auth import StartState
from src.loader import db
from src.keyboards.inline.start import choice_kb
from src.keyboards.inline.admin import admin_kb
from data.config import ADMIN_IDS
from src.utils.misc.throttling import rate_limit

@rate_limit(5, 'start')
async def register_user(msg: types.Message):
    # here check to user exists

    logger.info(f"Start register_user handler user_id: {msg.from_user.id}, chat_id: {msg.chat.id}")
    #if msg.from_user.id in ADMIN_IDS:
    #    logger.info('Admin logged in!')
    #    await msg.answer(
    #        "Вы авторизованы как админ, админ панель:",
    #        reply_markup=admin_kb,
    #    )
    #    return

    tg_user = types.User.get_current()
    user = await db.get_user(tg_user.id)

    if user and user.is_authed is True:
        return await msg.answer("Вы уже авторизованы как польветель!")

    return await msg.answer("Выбирите:", reply_markup=choice_kb)

@rate_limit(5, 'start')
async def log_in_user(call_back: types.CallbackQuery):
    await StartState.wait_to_login.set()

    await call_back.message.edit_text("Прежде чем пройти и использвать бота, авторизуйтесь! \n видите Логин или Имя")





