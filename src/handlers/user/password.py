from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from src.loader import db
from src.states.user.cng_pass import ChangePassword

async def get_password(user_id: int) -> Union[str, None]:
    user = await db.get_user(user_id)
    return user.password

async def start_change_password(msg: types.Message):
    tg_user = types.User.get_current()
    pass_ = await get_password(tg_user.id)
    logger.info(f"Starting to changing password: {tg_user.full_name}")

    if not pass_:
        return await msg.answer("Вы не авторизованы,\n из за этого вы не можете использвать эту комманду")

    await ChangePassword.wait_to_accept_with_password.set()
    await msg.answer("Хорошо, Напишите ваш пароль для доказательства что это вы")

async def check_to_really_user(msg: types.Message):
    tg_user = types.User.get_current()
    pass_ = await get_password(tg_user.id)

    if pass_ != msg.text:
        return await msg.answer("Ваш пароль, не верный попробуйте еще разок.\n Может тогда получится")
    else:
        await ChangePassword.wait_to_password.set()
        await msg.answer("Теперь, напишите новый пароль на который вы хотите сменить:")

async def change_password(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["password"] = msg.text

        await msg.delete()

    await msg.answer(f"Теперь вы уверены в этом ? Y | N: \nПароль на который вы хотите изменить: {msg.text}")
    await ChangePassword.wait_to_accept_pass.set()

async def changing_fully(msg: types.Message, state: FSMContext):
    if msg.text in ["Y", "y", "yes", "yeah", "да"]:
        async with state.proxy() as data:
            password = data["password"]
            tg_user = types.User.get_current()
            user = await db.get_user(tg_user.id)

            await msg.delete()

            await user.update(password=password).apply()

            await msg.answer("Успех вы сменили пароль!")
    elif msg.text in ["N", "n", "нет", "no"]:
        await msg.answer("Вы отменили изменение пароля!")
    else:
        return await msg.answer("Некорректный ввод! Y | N:")
    await state.finish()

