import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from iternal.bot.loader import dp, db
from iternal.bot.states.user.sign_in import SignIn


@dp.callback_query_handler(text="sign_in", state="*")
async def signin_start(cq: types.CallbackQuery) -> None:
    _t = cq.message.answer("Видите логин своего аккаунта.")
    await _t
    await SignIn.wait_login.set()


@dp.message_handler(state=SignIn.wait_login, content_types="TEXT")
async def signin_name(m: types.Message, state: FSMContext) -> None:
    await m.answer("Введите Пароль от своего аккаунта")
    await state.update_data({"si_login": m.text})
    await SignIn.wait_password.set()


@dp.message_handler(state=SignIn.wait_password, content_types="TEXT")
async def signin_final(m: types.Message, state: FSMContext):
    password = m.text
    async with state.proxy() as data:
        login = data['si_name']
    u = await db.get_user_name3password(login, password)
    tasks = [m.delete()]
    if u is not None:
        tasks.append(m.answer("Хорошо вы зашли в свой аккаунт"))
    else:
        tasks.append(m.answer("Повторите снова, или зайдите в свой аккаунт"))

    await asyncio.gather(*tasks)
