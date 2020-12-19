from aiogram import types
from aiogram.dispatcher import FSMContext

from src.loader import db
from src.states.user.cng_email import ChangeEmail

async def start_change_email(msg: types.Message):
    user = await db.get_user(msg.from_user.id)

    if not user:
        return

    await msg.answer("Хорошо Ввидите Емейл на который вы хотите Сменить")
    await ChangeEmail.wait_to_email.set()

async def change_email_input(msg: types.Message, state: FSMContext):
    if len(msg.text) >= 200:
        return await msg.answer("Лимит в 200 сиволов, больше нельзя!")

    if not '@' in msg.text:
        return await msg.answer("Некорректный эмейл, не содержится знака '@' в эмейле")

    async with state.proxy() as data:
        data["email"] = msg.text

    await ChangeEmail.wait_to_accept.set()
    await msg.answer("Теперь вы Уверены в этом ? Y/N")


async def accept_and_complete_emailcng(msg: types.Message, state: FSMContext):
    if msg.text.lower() == 'y':
        user = await db.get_user(msg.from_user.id)

        async with state.proxy() as data:
            email = data["email"]

        await user.update(email=email).apply()
        await state.finish()
        await msg.answer("Успех, Вы поменяли Свои Эмейл")
    elif msg.text.lower() == 'n':
        await state.finish()
        return await msg.answer("Действие отменено")
    else:
        await msg.answer("Ошибка в вводе!")