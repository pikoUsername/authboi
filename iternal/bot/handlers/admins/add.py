from aiogram import types
from aiogram.dispatcher.webhook import SendMessage

from iternal.bot.loader import dp, db
from iternal.bot.utils.spammer import notify_all_admins


@dp.message_handler(commands="set_admin", is_authed=True, is_admin=True)
async def set_admin_user(msg: types.Message):
    args = msg.get_args()

    if not args or not args[0].isdigit():
        return False

    args = args.split()
    user_id = int(args[0])
    remove = len(args) == 2 and args[1] == "-rm"

    try:
        await db.create_admin_user(user_id, remove)
    except ValueError:
        return SendMessage(msg.chat.id, "Такого Пользветеля Не Существует")
    await msg.answer(
        "Успех, Статус пользветеля Обновлен. Высылается Всем Админом о Добовления Админа"
    )

    result = await notify_all_admins(text=f"Был Обновлен Статус Пользветелья с именем {msg.from_user.last_name}")
    return SendMessage(msg.chat.id, "\n".join(result))
