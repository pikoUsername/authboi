from aiogram import types
from aiogram.dispatcher.filters import Command

from src.loader import dp, db
from src.utils.checks import check_for_admin


@dp.message_handler(commands="set_admin")
async def set_admin_user(msg: types.Message):
    await check_for_admin(msg, msg.from_user.id)

    args = msg.get_args()
    if not args or not args[0].isdigit():
        return False
    args = args.split()
    user_id = int(args[0])
    remove = len(args) == 2 and args[1] == "-rm"

    try:
        result = await db.create_admin_user(user_id, remove)
    except ValueError:
        result = None

    if result:
        return await msg.answer(
            f"Успех, Вы дали {user_id} Админ Права"
        )
    return await msg.answer(
        f"Ошибка Не смог дать {user_id} Админ Права"
    )