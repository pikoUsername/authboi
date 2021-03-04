from typing import Optional

from aiogram import Dispatcher

from iternal.bot.utils.embed import Embed


def fill_auth_final(password: str, login: str, email: str) -> Optional[str]:
    pass_to_show = ["*" for _ in range(len(password))]

    e = Embed("Профиль: ")

    e.add_field("Имя", login)
    e.add_field("email", email)
    e.add_field("Пароль", "".join(pass_to_show))

    return e.clean_embed


async def close_webhook(dp: Dispatcher):
    await dp.bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
