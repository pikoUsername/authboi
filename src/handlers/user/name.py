from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
from loguru import logger

from src.states.user.cng_name import ChangeName
from src.loader import db, dp

@dp.message_handler(commands="change_name", state="*")
async def start_change_name(msg: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        return

    user = await db.get_user(msg.from_user.id)

    if not user:
        return

    await msg.answer("Хорошо, скажите имя на которое вы хотите сменить")
    await ChangeName.wait_to_name.set()


@dp.message_handler(state=ChangeName.wait_to_name, content_types=ContentType.TEXT)
async def wait_to_name_(msg: types.Message, state: FSMContext):
    if ' ' in msg.text or len(msg.text) >= 200:
        return await msg.answer("Не допустимое Имя, Есть пробел в Имени или оно прывышает лимит в 200 знаков!")

    async with state.proxy() as data:
        data["Name"] = msg.text

    await msg.answer("Вы точно уверены об Этом? Y/N:")
    await ChangeName.wait_to_accept.set()


@dp.message_handler(text=("Y", "y"), state=ChangeName.wait_to_accept)
async def accept_change_name(msg: types.Message, state: FSMContext):
    user = await db.get_user(msg.from_user.id)
    async with state.proxy() as data:
        name = data["Name"]

    try:
        await user.update(login=name).apply()
        await msg.answer(f"Успех Вы поменяли свое Имя! теперь вы {name}")
    except Exception as e:
        logger.exception(e)
        await msg.answer("Измение прошла плохо, попробуйте снова")
    await state.finish()


@dp.message_handler(text=("N", "n"), state=ChangeName.wait_to_accept)
async def cancel_change_name(msg: types.Message, state: FSMContext):
    await msg.answer("Вы отменили действие")
    await state.finish()


@dp.message_handler(state=ChangeName.wait_to_accept)
async def accept_to_change_name(msg: types.Message, state: FSMContext):
    return await msg.answer("Повторите действие или выйдите /cancel или N")


