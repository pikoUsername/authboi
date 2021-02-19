from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import ctx_data
from aiogram.dispatcher.webhook import SendMessage
from aiogram.types import ContentType
from loguru import logger

from src.loader import dp
from src.models.user import User
from src.states.user.desc import DescriptionChange


@dp.message_handler(commands="change_description", is_authed=True, state="*")
async def start_change_description(msg: types.Message):
    logger.info("here changing description")
    await DescriptionChange.wait_to_description.set()
    return SendMessage(msg.chat.id, "Теперь ввидите Описание вашего профиля.")


@dp.message_handler(state=DescriptionChange.wait_to_description, content_types=ContentType.TEXT)
async def change_description(msg: types.Message, state: FSMContext):
    if not msg.text:
        return SendMessage(msg.chat.id, "Вы нечего не ввели, это не допустимо!")

    async with state.proxy() as data:
        data["description"] = msg.text

    await DescriptionChange.wait_to_accept_change.set()
    return SendMessage(msg.chat.id, "Теперь вы уверены в своем выборе? Y|N")


@dp.message_handler(text=("Y", "y", "yes"), state=DescriptionChange.wait_to_accept_change)
async def yes_change_desc(msg: types.Message, state: FSMContext, user: User):
    async with state.proxy() as data:
        description = data["description"]

    await user.update(description=description).apply()

    await state.finish()
    return SendMessage(msg.chat.id, "Вашо описание профиля было измнено.")


@dp.message_handler(text=("N", "no", "n"), state=DescriptionChange.wait_to_accept_change)
async def cancel_change_desc(msg: types.Message, state: FSMContext):
    await state.finish()
    return SendMessage(msg.chat.id, "Вы отменили изменения описания профиля.")


@dp.message_handler(state=DescriptionChange.wait_to_accept_change, content_types=ContentType.TEXT)
async def accept_change_description(msg: types.Message):
    return SendMessage(msg.chat.id, "Неправльные аргумент, попробуйте снова!")
