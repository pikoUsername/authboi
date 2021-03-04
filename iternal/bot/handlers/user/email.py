from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.webhook import SendMessage
from aiogram.types import ContentType

from iternal.bot.loader import dp
from iternal.bot.states.user.cng_email import ChangeEmail
from iternal.store.user import User


@dp.message_handler(commands="change_email", is_authed=True, state="*")
async def start_change_email(msg: types.Message):
    await ChangeEmail.wait_to_email.set()
    async with SendMessage() as mes:
        # yes, its working, lol
        mes.text = "Хорошо, Введите Емейл на который вы хотите сменить."
        mes.chat_id = msg.chat.id


@dp.message_handler(state=ChangeEmail.wait_to_email, content_types=ContentType.TEXT)
async def change_email_input(msg: types.Message, state: FSMContext):
    if len(msg.text) >= 200:
        return SendMessage(msg.chat.id, "Лимит в 200 сиволов, больше нельзя!")

    if '@' not in msg.text:
        return SendMessage(msg.chat.id, "Некорректный эмейл, не содержится знака '@' в эмейле.")

    await state.update_data(email=msg.text)

    await ChangeEmail.wait_to_accept.set()
    return SendMessage(msg.chat.id, "Теперь вы Уверены в этом? Y/N")


@dp.message_handler(text=("Y", "y", "yes"), state=ChangeEmail.wait_to_accept)
async def accept_change_email(msg: types.Message, state: FSMContext, user: User):
    async with state.proxy() as data:
        email = data["email"]

    try:
        await user.update(email=email).apply()
    except TypeError:
        return SendMessage(msg.chat.id, "Ошибка, Невозможно Сменить Эмейл.")
    await state.finish()
    return SendMessage(msg.chat.id, "Успех, Вы поменяли Свой Эмейл.")


@dp.message_handler(text=("N", "n", "no"), state=ChangeEmail.wait_to_accept)
async def cancel_change_email(msg: types.Message, state: FSMContext):
    await state.finish()
    return SendMessage(msg.chat.id, "Действие отменено.")


@dp.message_handler(state=ChangeEmail.wait_to_accept, content_types=ContentType.TEXT)
async def email_not(msg: types.Message):
    return SendMessage(msg.chat.id, "Ошибка в вводе!")
