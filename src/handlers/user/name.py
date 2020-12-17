from aiogram import types
from aiogram.dispatcher import FSMContext

from src.states.user.cng_name import ChangeName
from src.loader import db

async def start_change_name(msg: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state:
        return

    user = await db.get_user(msg.from_user.id)

    if not user:
        return

    await msg.answer("Хорошо, скажите имя на которое вы хотите сменить")
    await ChangeName.wait_to_name.set()

async def wait_to_name_(msg: types.Message, state: FSMContext):
    if ' ' in msg.text or len(msg.text) >= 200:
        return await msg.answer("Не допустимое Имя, Есть пробел в Имени или оно прывышает лимит в 200 знаков!")

    async with state.proxy() as data:
        data["Name"] = msg.text

    await msg.answer("Вы точно уверены об Этом? Y/N:")
    await ChangeName.wait_to_accept.set()

async def accept_to_change_name(msg: types.Message, state: FSMContext):
    if msg.text.lower() == "y":
        user = await db.get_user(msg.from_user.id)
        async with state.proxy() as data:
            name = data["Name"]

        await msg.answer(f"Успех Вы поменяли свое Имя! теперь вы {name}")

        await state.finish()
        return await user.update(login=name).apply()
    elif msg.text.lower() == "n":
        await msg.answer("Вы отменили действие")
        return await state.finish()
    else:
        await msg.answer("Повторите действие или выйдите /cancel или N")


