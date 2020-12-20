from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ContentType
from loguru import logger

from src.loader import db, dp
from src.states.user.cng_pass import ChangePassword
from src.utils.throttling import rate_limit


async def get_password(user_id: int):
    user = await db.get_user(user_id)
    if not user:
        return
    return user.password

@dp.message_handler(Command("change_password"), state="*")
@rate_limit(5, 'change_password')
async def start_change_password(msg: types.Message):
    """
    starting change password
    registered in 52 line of __init__.py
    """
    tg_user = types.User.get_current()
    pass_ = await get_password(tg_user.id)
    logger.info(f"Starting to changing password: {tg_user.full_name}")

    if not pass_:
        return

    await ChangePassword.wait_to_accept_with_password.set()
    await msg.answer("Хорошо, Напишите ваш пароль для доказательства что это вы")


@dp.message_handler(state=ChangePassword.wait_to_accept_with_password)
async def check_to_really_user(msg: types.Message):
    tg_user = types.User.get_current()
    pass_ = await get_password(tg_user.id)

    if pass_ != msg.text:
        return await msg.answer("Ваш пароль, не верный попробуйте еще разок.\n Может тогда получится")
    else:
        await ChangePassword.wait_to_password.set()
        await msg.answer("Теперь, напишите новый пароль на который вы хотите сменить:")


@dp.message_handler(state=ChangePassword.wait_to_password, content_types=ContentType.TEXT)
async def change_password(msg: types.Message, state: FSMContext):
    """
    checks msg.text for long and spaces in text
    refistered on 51 line of __init__.py
    """
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


@dp.message_handler(state=ChangePassword.wait_to_accept_pass, content_types=ContentType.TEXT)
async def changing_fully(msg: types.Message, state: FSMContext):
    """
    accept and changing password for User
    registered in 58 line in __init__.py
    """
    if msg.text in ["Y", "y", "yes", "yeah", "да"]:
        async with state.proxy() as data:
            logger.info(f"user: {msg.from_user.username}, changed password")
            password = data["password"]

        user = await db.get_user(msg.from_user.id)

        await user.update(password=password).apply()

        await msg.answer("Успех вы сменили пароль!")
    elif msg.text in ["N", "n", "нет", "no"]:
        await msg.answer("Вы отменили изменение пароля!")
    else:
        return await msg.answer("Некорректный ввод! Y | N:")
    await state.finish()

