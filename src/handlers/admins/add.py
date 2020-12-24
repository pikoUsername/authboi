from aiogram import types
from aiogram.dispatcher.filters import Command

from src.loader import dp, db


@dp.message_handler(Command("set_admin"))
async def set_admin_user(msg: types.Message):
    user = await db.get_user(msg.from_user.id)

    if not user:
        return await msg.answer("Вы не Авторизованы")

    if not user.is_admin:
        return False

    args = msg.get_args()
    if not args or not args[0].isdigit():
        return False
    args = args.split()
    user_id = int(args[0])
    remove = len(args) == 2 and args[1] == "-rm"

    try:
        result = await db.create_admin_user(user_id, remove)
    except ValueError:
        result = False

    if result:
        return await msg.answer(
            f"Успех, Вы дали {user_id} Админ Права"
        )
    return await msg.answer(
        f"Ошибка Не смог дать {user_id} Админ Права"
    )