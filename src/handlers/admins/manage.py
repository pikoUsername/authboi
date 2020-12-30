from aiogram import types

from src.loader import dp, db
from src.utils import is_admin

@dp.message_handler(commands="delete_user", state="*")
@is_admin
async def delete_user_from_db(msg: types.Message):
    args = msg.get_args()
    user_id = args[0]

    try:
        result = await db.remove_user(user_id)
    except ValueError:
        result = False

    if not result:
        return await msg.answer("Пользветель Не Найден!")
    await msg.answer("Пользветель Был Удален")
