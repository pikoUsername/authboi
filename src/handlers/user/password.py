from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.handler import ctx_data
from aiogram.dispatcher.webhook import SendMessage
from aiogram.types import ContentType
from loguru import logger

from src.loader import dp
from src.states.user.cng_pass import ChangePassword
from src.utils.throttling import rate_limit


@dp.message_handler(commands="change_password", is_authed=True, state="*")
@rate_limit(5, 'change_password')
async def start_change_password(msg: types.Message):
    logger.info(f"Starting to changing password: {msg.from_user.full_name}")

    await ChangePassword.wait_to_accept_with_password.set()
    return SendMessage(msg.chat.id, "Хорошо, Напишите ваш пароль для доказательства что это вы")


@dp.message_handler(state=ChangePassword.wait_to_accept_with_password)
async def check_to_really_user(msg: types.Message):
    data = ctx_data.get()
    user = data["user"]

    if user.password != msg.text:
        return SendMessage(msg.chat.id, "Ваш пароль, не верный попробуйте еще разок.\n Может тогда получится")
    await ChangePassword.wait_to_password.set()
    return SendMessage(msg.chat.id, "Теперь, напишите новый пароль на который вы хотите сменить:")


@dp.message_handler(state=ChangePassword.wait_to_password, content_types=ContentType.TEXT)
async def change_password(msg: types.Message, state: FSMContext):
    if len(msg.text) <= 8:
        return SendMessage(msg.chat.id, "Недопустимый пароль, он должен прывышать длинну 8 знаков")
    elif ' ' in msg.text:
        return SendMessage(msg.chat.id, "Недопустимый пароль, он содержит пробелы, это недпоустимо!")
    elif len(msg.text) >= 200:
        return SendMessage(msg.chat.id, "Недопустимый пароль, он прывышает 200 сиволов")

    async with state.proxy() as data:
        data["password"] = msg.text

        await msg.delete()

    await ChangePassword.wait_to_accept_pass.set()
    return SendMessage(msg.chat.id,
                       f"Теперь вы уверены в этом ? Y | N:")


@dp.message_handler(text=("Y", "y", "yes"), state=ChangePassword.wait_to_accept_pass)
async def accept_change_password(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        logger.info(f"user: {msg.from_user.username}, changed password")
        password = data["password"]

    data = ctx_data.get()
    user = data["user"]
    try:
        await user.update(password=password).apply()
        await state.finish()
    except Exception as e:
        return SendMessage(msg.chat.id, str(e))
    else:
        return SendMessage(msg.chat.id, "Успех вы сменили пароль!")


@dp.message_handler(text=("N", "n", "no"), state=ChangePassword.wait_to_accept_pass)
async def cancel_change_password(msg: types.Message, state: FSMContext):
    await state.finish()
    return SendMessage(msg.chat.id, "Вы отменили изменение пароля!")


@dp.message_handler(state=ChangePassword.wait_to_accept_pass, content_types=ContentType.TEXT)
async def changing_fully(msg: types.Message):
    return SendMessage(msg.chat.id, "Некорректный ввод! Y | N:")
