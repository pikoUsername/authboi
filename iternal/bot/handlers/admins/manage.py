from aiogram import types
from aiogram.dispatcher.webhook import SendMessage

from iternal.bot.loader import dp, db


@dp.message_handler(commands="delete_user", is_admin=True, state="*")
async def delete_user_from_db(msg: types.Message):
    args = msg.get_args()
    try:
        user_id = int(args[1])
    except IndexError:
        return SendMessage(msg.chat.id, "Не Указан Обезательный Аргумент")
    try:
        result = await db.remove_user(user_id)
    except AttributeError:
        result = None

    if not result:
        return await msg.answer("Пользветель Не Найден!")
    await msg.answer("Пользветель Был Удален")
