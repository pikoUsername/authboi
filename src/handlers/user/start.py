from aiogram import types

from src.states.user.auth import StartState
from src.states.user.sign_up import SignIn
from src.loader import db
from src.keyboards.inline.start import choice_kb
from src.keyboards.inline.admin import admin_kb
from data.config import ADMIN_IDS

async def register_user(msg: types.Message):
    # here check to user exists
    tg_user = types.User.get_current()
    if tg_user.id in ADMIN_IDS:
        return await msg.answer(
            "Вы авторизованы как админ, админ панель:",
            reply_markup=admin_kb,
        )

    user = await db.get_user(tg_user.id)

    if user and user.is_authed is True:
        return await msg.answer("Вы уже авторизованы как польветель! Если хотите выйти то комманда exit!")

    return await msg.answer("Выбирите:", reply_markup=choice_kb)

async def log_in_user(call_back: types.CallbackQuery):
    await StartState.wait_to_login.set()

    await call_back.message.reply("Прежде чем пройти и использвать бота, авторизуйтесь! \n Предупреждение! Вы будете вышвернуты с аккаунта если будете уверены об этом пуоступке")

async def sign_in_user(call_back: types.CallbackQuery):
    await SignIn.wait_to_type_login.set()

    await call_back.message.answer("Ввидите ваш Логин или Имя!")





