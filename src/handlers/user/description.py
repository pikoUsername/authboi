from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ContentType
from loguru import logger

from src.loader import db, dp
from src.states.user.desc import DescriptionChange

@dp.message_handler(Command("change_description"), state="*")
async def start_change_description(msg: types.Message):
    user = await db.get_user(msg.from_user.id)

    if not user:
        return await msg.answer("Вы не авторизованы как пользветель!")

    logger.info("here changing description")
    await DescriptionChange.wait_to_description.set()
    await msg.answer("Теперь ввидите Описание вашего профиля!")

@dp.message_handler(state=DescriptionChange.wait_to_description, content_types=ContentType.TEXT)
async def change_description(msg: types.Message, state: FSMContext):
    if not msg.text:
        return await msg.answer("ВЫ нечего не ввели, это не допустимо!")

    async with state.proxy() as data:
        data["description"] = msg.text

    await DescriptionChange.wait_to_accept_change.set()
    return await msg.answer("Теперь вы уверены в своем выборе? Y|N")


@dp.message_handler(state=DescriptionChange.wait_to_accept_change, content_types=ContentType.TEXT)
async def accept_change_description(msg: types.Message, state: FSMContext):
    if msg.text in ["Y", "y", "yes", "да"]:
        async with state.proxy() as data:
            description = data["description"]

        user = await db.get_user(msg.from_user.id)
        await user.update(description=description).apply()

        await msg.answer("Вашо описание профиля было измнено")
    elif msg.text in ["N", "n", "no", "nooooo"] or 'n' in msg.text:
        await msg.answer("Вы отменили изменения описания профиля!")
    else:
        return await msg.answer("НЕправльные аргумент, попробуйте снова!")
    await state.finish()
