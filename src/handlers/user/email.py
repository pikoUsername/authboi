from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ContentType

from src.loader import db, dp
from src.states.user.cng_email import ChangeEmail


@dp.message_handler(Command("change_email"), state="*")
async def start_change_email(msg: types.Message):
    user = await db.get_user(msg.from_user.id)

    if not user:
        return

    await msg.answer("Хорошо Ввидите Емейл на который вы хотите Сменить")
    await ChangeEmail.wait_to_email.set()


@dp.message_handler(state=ChangeEmail.wait_to_email, content_types=ContentType.TEXT)
async def change_email_input(msg: types.Message, state: FSMContext):
    if len(msg.text) >= 200:
        return await msg.answer("Лимит в 200 сиволов, больше нельзя!")

    if not '@' in msg.text:
        return await msg.answer("Некорректный эмейл, не содержится знака '@' в эмейле")

    async with state.proxy() as data:
        data["email"] = msg.text

    await ChangeEmail.wait_to_accept.set()
    await msg.answer("Теперь вы Уверены в этом ? Y/N")


@dp.message_handler(Text(["Y", "y", "yes"]), state=ChangeEmail.wait_to_accept)
async def accept_change_email(msg: types.Message, state: FSMContext):
    user = await db.get_user(msg.from_user.id)

    async with state.proxy() as data:
        email = data["email"]

    await user.update(email=email).apply()
    await state.finish()
    await msg.answer("Успех, Вы поменяли Свои Эмейл")


@dp.message_handler(Text(["N", "n", "no"]), state=ChangeEmail.wait_to_accept)
async def cancel_change_email(msg: types.Message, state: FSMContext):
    await state.finish()
    return await msg.answer("Действие отменено")


@dp.message_handler(state=ChangeEmail.wait_to_accept, content_types=ContentType.TEXT)
async def accept_and_complete_emailcng(msg: types.Message, state: FSMContext):
    await msg.answer("Ошибка в вводе!")
