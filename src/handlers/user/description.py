from aiogram import types
from aiogram.dispatcher import FSMContext

from src.loader import db
from src.states.user.desc import DescriptionChange

async def start_change_description(msg: types.Message):
    tg_user = types.User.get_current()
    user = await db.get_user(tg_user.id)

    if not user:
        return await msg.answer("Вы не авторизованы как пользветель!")

    await DescriptionChange.wait_to_description.set()
    await msg.answer("Теперь ввидите Описание вашего профиля!")

async def change_description(msg: types.Message, state: FSMContext):
    if not msg.text:
        return await msg.answer("ВЫ нечего не ввели, это не допустимо!")

    async with state.proxy() as data:
        data["description"] = msg.text

    await DescriptionChange.wait_to_accept_change.set()
    return await msg.answer("Теперь вы уверены в своем выборе? Y|N")

async def accept_change_description(msg: types.Message, state: FSMContext):
    if msg.text in ["Y", "y", "yes", "да"] or 'y' in msg.text:
        async with state.proxy() as data:
            description = data["description"]
            tg_user = types.User.get_current()
            user = await db.get_user(tg_user.id)

            user.description = description
    elif msg.text in ["N", "n", "no", "nooooo"] or 'n' in msg.text:
        await msg.answer("Вы отменили изменения описания профиля!")
    else:
        return await msg.answer("НЕправльные аргумент, попробуйте снова!")
    await state.finish()
