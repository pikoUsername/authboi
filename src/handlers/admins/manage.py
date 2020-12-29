from aiogram import types

from src.models.models import User
from src.loader import dp
from src.utils import is_admin

@dp.message_handler(commands="delete_user", state="*")
@is_admin
async def delete_user_from_db(msg: types.Message):
    args = msg.get_args()

    user_id = args[0]
    user = await User.query.where(User.user_id == user_id).gino.first()

    if not user:
        return await msg.reply("Пользветель Не сущесвует")

    try:
        await user.delete()
    except Exception as e:
        return await msg.reply(str(e), reply=False)
    await msg.answer("Пользветель Был Удален")
