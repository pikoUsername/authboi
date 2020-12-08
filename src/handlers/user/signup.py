from aiogram import types
from aiogram.dispatcher import FSMContext

from src.loader import db
from src.states.user.sign_up import SignIn

# any state check for user auth, __init__ in file have handlers message
async def start_sign_in(call_back: types.CallbackQuery):
    await SignIn.wait_to_type_login()

    await call_back.message.edit_text("Введите Логин или имя вашего аккаунта!")


async def login_sign_in(message: types.Message, state: FSMContext):
    user_login = await db.get_user_by_login(message.text)
    with state.proxy() as data:
        data["user_login"] = user_login
        await SignIn.wait_to_type_password.set()
        return await message.answer("Теперь ввидите пароль! ")


async def password_sign_in(message: types.Message, state: FSMContext):
    user_authed_with_pass = await db.get_user_by_password(message.text)
    with state.proxy() as data:
        data["user_authed_with_pass"] = user_authed_with_pass

async def sign_in(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Эта комманда Не работает!")
    pass

