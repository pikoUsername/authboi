from aiogram import types

from src.loader import dp, db
from src.utils.checks import check_for_admin


@dp.message_handler(commands="delete_user", state="*")
async def delete_user_from_db(msg: types.Message):
    res = await check_for_admin(msg, msg.from_user.id)
    if not res:
        return
    args = msg.get_args()
    try:
        user_id = int(args[1])
    except IndexError:
        return await msg.answer("Не Указан Обезательный Аргумент")
    try:
        result = await db.remove_user(user_id)
    except ValueError:
        result = False

    if not result:
        return await msg.answer("Пользветель Не Найден!")
    await msg.answer("Пользветель Был Удален")
