from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ContentType
from loguru import logger

from src.loader import db, dp
from src.states.user.cng_pass import ChangePassword
from src.utils.throttling import rate_limit

@dp.message_handler(Command("change_password"), state="*")
@rate_limit(5, 'change_password')
async def start_change_password(msg: types.Message):
    pass_ = await db.get_user(msg.from_user.id)
    logger.info(f"Starting to changing password: {msg.from_user.full_name}")

    if not pass_:
        return

    await ChangePassword.wait_to_accept_with_password.set()
    await msg.answer("Хорошо, Напишите ваш пароль для доказательства что это вы")


@dp.message_handler(state=ChangePassword.wait_to_accept_with_password)
async def check_to_really_user(msg: types.Message):
    pass_ = await db.get_user(msg.from_user.id)

    if pass_ != msg.text:
        return await msg.answer("Ваш пароль, не верный попробуйте еще разок.\n Может тогда получится")
    else:
        await ChangePassword.wait_to_password.set()
        await msg.answer("Теперь, напишите новый пароль на который вы хотите сменить:")


@dp.message_handler(state=ChangePassword.wait_to_password, content_types=ContentType.TEXT)
async def change_password(msg: types.Message, state: FSMContext):
    if len(msg.text) <= 8:
        return await msg.answer("Недопустимый пароль, он должен прывышать длинну 8 знаков")
    elif ' ' in msg.text:
        return await msg.answer("Недопустимый пароль, он содержит пробелы, это недпоустимо!")
    elif len(msg.text) >= 200:
        return await msg.answer("Недопустимый пароль, он прывышает 200 сиволов")

    async with state.proxy() as data:
        data["password"] = msg.text

        await msg.delete()

    await msg.answer(f"Теперь вы уверены в этом ? Y | N: \nПароль на который вы хотите изменить: {msg.text}")
    await ChangePassword.wait_to_accept_pass.set()

@dp.message_handler(Text(["Y", "y", "yes"]), state=ChangePassword.wait_to_accept_pass)
async def accept_change_password(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        logger.info(f"user: {msg.from_user.username}, changed password")
        password = data["password"]

    user = await db.get_user(msg.from_user.id)

    await user.update(password=password).apply()

    await msg.answer("Успех вы сменили пароль!")


@dp.message_handler(Text(["N", "n", "no"]), state=ChangePassword.wait_to_accept_pass)
async def cancel_change_password(msg: types.Message, state: FSMContext):
    await msg.answer("Вы отменили изменение пароля!")
    await state.finish()


@dp.message_handler(state=ChangePassword.wait_to_accept_pass, content_types=ContentType.TEXT)
async def changing_fully(msg: types.Message, state: FSMContext):
    return await msg.answer("Некорректный ввод! Y | N:")

