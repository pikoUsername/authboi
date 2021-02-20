from typing import Optional

from aiogram import Dispatcher


def fill_auth_final(password: str, login: str, email: str) -> Optional[str]:
    password_len = len(password)
    pass_to_show = []
    for i in range(0, password_len):
        pass_to_show.append("*")

    text = [
        "Вы авторизованы как: ",
        f"Имя: {login}",
        f"email: {email}",
        "Пароль: ",
        "".join(pass_to_show),
    ]
    return "\n".join(text)


async def close_webhook(dp: Dispatcher):
    await dp.bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()