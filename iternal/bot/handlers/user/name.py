from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.webhook import SendMessage
from aiogram.types import ContentType
from loguru import logger

from iternal.bot.states.user.cng_name import ChangeName
from iternal.bot.loader import db, dp
from iternal.store.user import User


@dp.message_handler(commands="change_name", is_authed=True, state="*")
async def start_change_name(msg: types.Message, state: FSMContext, user: User):
    current_state = await state.get_state()
    if user is None or current_state is None:
        return

    await msg.answer("Хорошо, скажите имя на которое вы хотите сменить")
    await ChangeName.wait_to_name.set()


@dp.message_handler(state=ChangeName.wait_to_name, content_types=ContentType.TEXT)
async def wait_to_name_(msg: types.Message, state: FSMContext):
    if msg.text.isspace() or len(msg.text) >= 200:
        return await msg.answer("Не допустимое Имя, Есть пробел в Имени или оно прывышает лимит в 200 знаков!")

    async with state.proxy() as data:
        data["Name"] = msg.text

    await ChangeName.wait_to_accept.set()
    return SendMessage(chat_id=msg.chat.id, text="Вы точно уверены об Этом? Y/N:")


@dp.message_handler(text=("Y", "y"), state=ChangeName.wait_to_accept)
async def accept_change_name(msg: types.Message, state: FSMContext):
    user = await db.get_user(msg.from_user.id)
    async with state.proxy() as data:
        name = data["Name"]

    try:
        await user.update(login=name).apply()
        await msg.answer(f"Успех Вы поменяли свое Имя! теперь ваше имя: {name}")
    except Exception as e:
        logger.exception(e)
        await msg.answer("Изменние Вызвали ошибки в СУБД, попробуйте снова!")
    await state.finish()


@dp.message_handler(text=("N", "n"), state=ChangeName.wait_to_accept)
async def cancel_change_name(msg: types.Message, state: FSMContext):
    await state.finish()
    return SendMessage(chat_id=msg.chat.id, text="Вы отменили действие.")


@dp.message_handler(state=ChangeName.wait_to_accept)
async def accept_to_change_name(msg: types.Message):
    return SendMessage(chat_id=msg.chat.id, text="Повторите действие или выйдите /cancel или N.")
